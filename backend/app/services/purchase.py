import os
import re
import uuid
import shutil
from datetime import datetime, date
from typing import List, Optional, Tuple, Dict, Any
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_, and_, case

from app.models.purchase import (
    Supplier,
    MaterialCategory,
    MaterialUnit,
    Material,
    StockLocation,
    Purchase,
    PurchaseLine,
    PurchaseReceipt,
    PurchaseReceiptItem,
    StockMovement,
    StockInventory,
    StockInventoryItem,
    PurchaseDocument,
)
from app.models.chantier import Chantier
from app.models.task import Task
from app.schemas.purchase import (
    SupplierCreate,
    SupplierUpdate,
    MaterialCategoryCreate,
    MaterialCategoryUpdate,
    MaterialUnitCreate,
    MaterialUnitUpdate,
    MaterialCreate,
    MaterialUpdate,
    StockLocationCreate,
    StockLocationUpdate,
    PurchaseCreate,
    PurchaseUpdate,
    QuickPurchaseCreate,
    PurchaseReceiptCreate,
    StockMovementCreate,
    StockTransferCreate,
    StockReturnCreate,
    StockInventoryCreate,
    StockInventoryUpdate,
    StockInventoryItemCreate,
)


UPLOAD_DIR = "uploads/purchases"


class PurchaseService:
    def __init__(self, db: Session):
        self.db = db

    # =========================================================================
    # 1. AUTO-GÉNÉRATEURS DE CODES & RÉFÉRENCES
    # =========================================================================
    def generate_supplier_code(self) -> str:
        """Génère le code fournisseur suivant: FOUR-001, FOUR-002..."""
        pattern = re.compile(r"^FOUR-(\d+)$")
        existing_codes = self.db.query(Supplier.code).filter(Supplier.code.like("FOUR-%")).all()
        max_seq = 0
        for (code,) in existing_codes:
            if code:
                m = pattern.match(code.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"FOUR-{(max_seq + 1):03d}"

    def generate_material_code(self) -> str:
        """Génère le code matériau suivant: MAT-YYYY-001, MAT-YYYY-002..."""
        year = datetime.now().year
        prefix = f"MAT-{year}-"
        pattern = re.compile(rf"^MAT-{year}-(\d+)$")
        existing_codes = self.db.query(Material.code).filter(Material.code.like(f"{prefix}%")).all()
        max_seq = 0
        for (code,) in existing_codes:
            if code:
                m = pattern.match(code.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"MAT-{year}-{(max_seq + 1):03d}"

    def generate_location_code(self) -> str:
        """Génère le code dépôt suivant: DEP-01, DEP-02..."""
        pattern = re.compile(r"^DEP-(\d+)$")
        existing_codes = self.db.query(StockLocation.code).filter(StockLocation.code.like("DEP-%")).all()
        max_seq = 0
        for (code,) in existing_codes:
            if code:
                m = pattern.match(code.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"DEP-{(max_seq + 1):02d}"

    def generate_purchase_ref(self) -> str:
        """Génère la référence achat: ACH-YYYY-00001, ACH-YYYY-00002..."""
        year = datetime.now().year
        prefix = f"ACH-{year}-"
        pattern = re.compile(rf"^ACH-{year}-(\d+)$")
        existing_refs = self.db.query(Purchase.reference).filter(Purchase.reference.like(f"{prefix}%")).all()
        max_seq = 0
        for (ref,) in existing_refs:
            if ref:
                m = pattern.match(ref.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"ACH-{year}-{(max_seq + 1):05d}"

    def generate_receipt_ref(self) -> str:
        """Génère le numéro de réception: REC-YYYY-00001..."""
        year = datetime.now().year
        prefix = f"REC-{year}-"
        pattern = re.compile(rf"^REC-{year}-(\d+)$")
        existing_refs = self.db.query(PurchaseReceipt.receipt_number).filter(PurchaseReceipt.receipt_number.like(f"{prefix}%")).all()
        max_seq = 0
        for (ref,) in existing_refs:
            if ref:
                m = pattern.match(ref.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"REC-{year}-{(max_seq + 1):05d}"

    def generate_movement_ref(self) -> str:
        """Génère la référence mouvement de stock: MVT-YYYY-00001..."""
        year = datetime.now().year
        prefix = f"MVT-{year}-"
        pattern = re.compile(rf"^MVT-{year}-(\d+)$")
        existing_refs = self.db.query(StockMovement.reference).filter(StockMovement.reference.like(f"{prefix}%")).all()
        max_seq = 0
        for (ref,) in existing_refs:
            if ref:
                m = pattern.match(ref.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"MVT-{year}-{(max_seq + 1):05d}"

    def generate_inventory_ref(self) -> str:
        """Génère la référence inventaire: INV-YYYY-001..."""
        year = datetime.now().year
        prefix = f"INV-{year}-"
        pattern = re.compile(rf"^INV-{year}-(\d+)$")
        existing_refs = self.db.query(StockInventory.reference).filter(StockInventory.reference.like(f"{prefix}%")).all()
        max_seq = 0
        for (ref,) in existing_refs:
            if ref:
                m = pattern.match(ref.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        pass
        return f"INV-{year}-{(max_seq + 1):03d}"

    # =========================================================================
    # 2. FOURNISSEURS (Suppliers)
    # =========================================================================
    def get_suppliers(
        self,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Supplier], int]:
        query = self.db.query(Supplier)
        if is_active is not None:
            query = query.filter(Supplier.is_active == is_active)
        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Supplier.name.ilike(s),
                    Supplier.code.ilike(s),
                    Supplier.phone.ilike(s),
                    Supplier.email.ilike(s),
                    Supplier.contact_name.ilike(s),
                )
            )
        total = query.count()
        suppliers = query.order_by(Supplier.name.asc()).offset(skip).limit(limit).all()
        return suppliers, total

    def get_supplier_by_id(self, supplier_id: int) -> Supplier:
        supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Fournisseur introuvable")
        return supplier

    def create_supplier(self, data: SupplierCreate) -> Supplier:
        # Code generation if empty
        code = (data.code.strip() if data.code else self.generate_supplier_code())
        # Check uniqueness
        if self.db.query(Supplier).filter(Supplier.code == code).first():
            code = self.generate_supplier_code()

        supplier = Supplier(
            code=code,
            name=data.name.strip(),
            trade_name=data.trade_name.strip() if data.trade_name else None,
            contact_name=data.contact_name.strip() if data.contact_name else None,
            phone=data.phone.strip(),
            email=data.email.strip() if data.email else None,
            address=data.address.strip() if data.address else None,
            city=data.city.strip() if data.city else "Abidjan",
            country=data.country.strip() if data.country else "Côte d'Ivoire",
            rccm=data.rccm.strip() if data.rccm else None,
            ncc=data.ncc.strip() if data.ncc else None,
            payment_terms=data.payment_terms.strip() if data.payment_terms else None,
            notes=data.notes.strip() if data.notes else None,
            is_active=data.is_active,
        )
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def update_supplier(self, supplier_id: int, data: SupplierUpdate) -> Supplier:
        supplier = self.get_supplier_by_id(supplier_id)
        update_data = data.model_dump(exclude_unset=True)

        if "code" in update_data and update_data["code"]:
            existing = self.db.query(Supplier).filter(
                Supplier.code == update_data["code"],
                Supplier.id != supplier_id,
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Ce code fournisseur existe déjà")

        for key, value in update_data.items():
            setattr(supplier, key, value)

        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def delete_supplier(self, supplier_id: int) -> bool:
        supplier = self.get_supplier_by_id(supplier_id)
        # Check if supplier has purchases
        has_purchases = self.db.query(Purchase).filter(Purchase.supplier_id == supplier_id).first()
        if has_purchases:
            # Soft delete by deactivating
            supplier.is_active = False
            self.db.commit()
            return True

        self.db.delete(supplier)
        self.db.commit()
        return True

    def get_supplier_stats(self, supplier_id: int) -> Dict[str, Any]:
        self.get_supplier_by_id(supplier_id)
        purchases = self.db.query(Purchase).filter(Purchase.supplier_id == supplier_id).all()
        total_orders = len(purchases)
        total_amount = sum(float(p.total_amount) for p in purchases)
        amount_paid = sum(float(p.total_amount) for p in purchases if p.payment_status == "Payé")
        # partially paid count as half or proportion
        amount_paid += sum(float(p.total_amount) * 0.5 for p in purchases if p.payment_status == "Partiellement payé")
        balance = total_amount - amount_paid

        return {
            "supplier_id": supplier_id,
            "total_orders": total_orders,
            "total_amount": total_amount,
            "amount_paid": amount_paid,
            "balance": balance,
        }

    # =========================================================================
    # 3. CATÉGORIES & UNITÉS DE MATÉRIAUX
    # =========================================================================
    def get_categories(self) -> List[MaterialCategory]:
        return self.db.query(MaterialCategory).order_by(MaterialCategory.name.asc()).all()

    def create_category(self, data: MaterialCategoryCreate) -> MaterialCategory:
        code = data.code.strip() if data.code else f"CAT-{data.name.upper()[:10].replace(' ', '_')}"
        existing = self.db.query(MaterialCategory).filter(
            or_(MaterialCategory.name == data.name.strip(), MaterialCategory.code == code)
        ).first()
        if existing:
            return existing

        category = MaterialCategory(
            code=code,
            name=data.name.strip(),
            description=data.description.strip() if data.description else None,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: int, data: MaterialCategoryUpdate) -> MaterialCategory:
        category = self.db.query(MaterialCategory).filter(MaterialCategory.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Catégorie introuvable")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        category = self.db.query(MaterialCategory).filter(MaterialCategory.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Catégorie introuvable")
        has_materials = self.db.query(Material).filter(Material.category_id == category_id).first()
        if has_materials:
            raise HTTPException(status_code=400, detail="Impossible de supprimer une catégorie liée à des matériaux")
        self.db.delete(category)
        self.db.commit()
        return True

    def get_units(self) -> List[MaterialUnit]:
        return self.db.query(MaterialUnit).order_by(MaterialUnit.name.asc()).all()

    def create_unit(self, data: MaterialUnitCreate) -> MaterialUnit:
        code = data.code.strip().upper()
        existing = self.db.query(MaterialUnit).filter(
            or_(MaterialUnit.code == code, MaterialUnit.name == data.name.strip())
        ).first()
        if existing:
            return existing

        unit = MaterialUnit(
            code=code,
            name=data.name.strip(),
        )
        self.db.add(unit)
        self.db.commit()
        self.db.refresh(unit)
        return unit

    def update_unit(self, unit_id: int, data: MaterialUnitUpdate) -> MaterialUnit:
        unit = self.db.query(MaterialUnit).filter(MaterialUnit.id == unit_id).first()
        if not unit:
            raise HTTPException(status_code=404, detail="Unité introuvable")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(unit, key, value)
        self.db.commit()
        self.db.refresh(unit)
        return unit

    def delete_unit(self, unit_id: int) -> bool:
        unit = self.db.query(MaterialUnit).filter(MaterialUnit.id == unit_id).first()
        if not unit:
            raise HTTPException(status_code=404, detail="Unité introuvable")
        has_materials = self.db.query(Material).filter(Material.unit_id == unit_id).first()
        if has_materials:
            raise HTTPException(status_code=400, detail="Impossible de supprimer une unité liée à des matériaux")
        self.db.delete(unit)
        self.db.commit()
        return True

    # =========================================================================
    # 4. MATÉRIAUX (Materials) & CALCUL DU STOCK
    # =========================================================================
    def calculate_material_stock(self, material_id: int, location_id: Optional[int] = None) -> float:
        """
        Calcule le stock physique actuel pour un matériau donné.
        Formule: (Entrée + Retour + Ajustement_pos + Transfert_in) - (Sortie + Ajustement_neg + Transfert_out)
        """
        query = self.db.query(StockMovement).filter(StockMovement.material_id == material_id)
        if location_id:
            query = query.filter(StockMovement.location_id == location_id)

        movements = query.all()
        stock = 0.0
        for m in movements:
            mtype = m.movement_type.strip().lower()
            if mtype in ["entrée", "entree", "retour"]:
                stock += abs(m.quantity)
            elif mtype in ["sortie"]:
                stock -= abs(m.quantity)
            elif mtype in ["transfert", "transfert in", "transfert out"]:
                # If movement_type is stored with sign
                stock += m.quantity
            elif mtype in ["ajustement", "inventaire"]:
                stock += m.quantity
            else:
                stock += m.quantity

        return max(0.0, round(stock, 2))

    def _enrich_material_dict(self, material: Material) -> Dict[str, Any]:
        """Convertit un Material en dictionnaire avec calcul du stock et statut."""
        current_stock = self.calculate_material_stock(material.id)
        if current_stock <= 0:
            stock_status = "Rupture"
        elif material.minimum_stock > 0 and current_stock <= material.minimum_stock:
            stock_status = "Stock faible"
        elif material.maximum_stock > 0 and current_stock > material.maximum_stock:
            stock_status = "Surstock"
        else:
            stock_status = "Normal"

        indicative_price = float(material.indicative_price or 0.0)
        stock_value = round(current_stock * indicative_price, 2)

        return {
            "id": material.id,
            "code": material.code,
            "name": material.name,
            "description": material.description,
            "category_id": material.category_id,
            "unit_id": material.unit_id,
            "reference": material.reference,
            "indicative_price": indicative_price,
            "minimum_stock": material.minimum_stock,
            "maximum_stock": material.maximum_stock,
            "is_active": material.is_active,
            "created_at": material.created_at,
            "updated_at": material.updated_at,
            "category": material.category,
            "unit": material.unit,
            "current_stock": current_stock,
            "stock_status": stock_status,
            "stock_value": stock_value,
        }

    def get_materials(
        self,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        stock_status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 200,
    ) -> Tuple[List[Dict[str, Any]], int]:
        query = self.db.query(Material).options(
            joinedload(Material.category),
            joinedload(Material.unit),
        )
        if category_id:
            query = query.filter(Material.category_id == category_id)
        if is_active is not None:
            query = query.filter(Material.is_active == is_active)
        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Material.name.ilike(s),
                    Material.code.ilike(s),
                    Material.reference.ilike(s),
                )
            )

        materials = query.order_by(Material.name.asc()).all()
        enriched = [self._enrich_material_dict(m) for m in materials]

        if stock_status_filter:
            enriched = [m for m in enriched if m["stock_status"].lower() == stock_status_filter.lower()]

        total = len(enriched)
        paginated = enriched[skip : skip + limit]
        return paginated, total

    def get_material_by_id(self, material_id: int) -> Dict[str, Any]:
        material = (
            self.db.query(Material)
            .options(joinedload(Material.category), joinedload(Material.unit))
            .filter(Material.id == material_id)
            .first()
        )
        if not material:
            raise HTTPException(status_code=404, detail="Matériau introuvable")
        return self._enrich_material_dict(material)

    def create_material(self, data: MaterialCreate) -> Dict[str, Any]:
        code = (data.code.strip() if data.code else self.generate_material_code())
        if self.db.query(Material).filter(Material.code == code).first():
            code = self.generate_material_code()

        material = Material(
            code=code,
            name=data.name.strip(),
            description=data.description.strip() if data.description else None,
            category_id=data.category_id,
            unit_id=data.unit_id,
            reference=data.reference.strip() if data.reference else None,
            indicative_price=data.indicative_price or 0.0,
            minimum_stock=data.minimum_stock or 0.0,
            maximum_stock=data.maximum_stock or 0.0,
            is_active=data.is_active,
        )
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return self.get_material_by_id(material.id)

    def update_material(self, material_id: int, data: MaterialUpdate) -> Dict[str, Any]:
        material = self.db.query(Material).filter(Material.id == material_id).first()
        if not material:
            raise HTTPException(status_code=404, detail="Matériau introuvable")

        update_data = data.model_dump(exclude_unset=True)
        if "code" in update_data and update_data["code"]:
            existing = self.db.query(Material).filter(
                Material.code == update_data["code"],
                Material.id != material_id,
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Ce code matériau existe déjà")

        for key, value in update_data.items():
            setattr(material, key, value)

        self.db.commit()
        return self.get_material_by_id(material.id)

    def delete_material(self, material_id: int) -> bool:
        material = self.db.query(Material).filter(Material.id == material_id).first()
        if not material:
            raise HTTPException(status_code=404, detail="Matériau introuvable")

        has_movements = self.db.query(StockMovement).filter(StockMovement.material_id == material_id).first()
        has_lines = self.db.query(PurchaseLine).filter(PurchaseLine.material_id == material_id).first()
        if has_movements or has_lines:
            material.is_active = False
            self.db.commit()
            return True

        self.db.delete(material)
        self.db.commit()
        return True

    # =========================================================================
    # 5. DÉPÔTS / EMPLACEMENTS DE STOCK
    # =========================================================================
    def get_locations(self, is_active: Optional[bool] = None) -> List[StockLocation]:
        query = self.db.query(StockLocation)
        if is_active is not None:
            query = query.filter(StockLocation.is_active == is_active)
        return query.order_by(StockLocation.name.asc()).all()

    def create_location(self, data: StockLocationCreate) -> StockLocation:
        code = data.code.strip() if data.code else self.generate_location_code()
        if self.db.query(StockLocation).filter(StockLocation.code == code).first():
            code = self.generate_location_code()

        location = StockLocation(
            code=code,
            name=data.name.strip(),
            location=data.location.strip() if data.location else None,
            type=data.type.strip() if data.type else "Dépôt principal",
            is_active=data.is_active,
        )
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def update_location(self, location_id: int, data: StockLocationUpdate) -> StockLocation:
        location = self.db.query(StockLocation).filter(StockLocation.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Emplacement introuvable")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(location, key, value)
        self.db.commit()
        self.db.refresh(location)
        return location

    def delete_location(self, location_id: int) -> bool:
        location = self.db.query(StockLocation).filter(StockLocation.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Emplacement introuvable")
        has_movements = self.db.query(StockMovement).filter(StockMovement.location_id == location_id).first()
        if has_movements:
            location.is_active = False
            self.db.commit()
            return True
        self.db.delete(location)
        self.db.commit()
        return True

    # =========================================================================
    # 6. ACHATS (Purchases)
    # =========================================================================
    def get_purchases(
        self,
        status_filter: Optional[str] = None,
        payment_status: Optional[str] = None,
        supplier_id: Optional[int] = None,
        chantier_id: Optional[int] = None,
        task_id: Optional[int] = None,
        is_quick_purchase: Optional[bool] = None,
        search: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Purchase], int]:
        query = (
            self.db.query(Purchase)
            .options(
                joinedload(Purchase.supplier),
                joinedload(Purchase.chantier),
                joinedload(Purchase.task),
                joinedload(Purchase.lines).joinedload(PurchaseLine.material).joinedload(Material.unit),
            )
        )

        if status_filter:
            query = query.filter(Purchase.status == status_filter)
        if payment_status:
            query = query.filter(Purchase.payment_status == payment_status)
        if supplier_id:
            query = query.filter(Purchase.supplier_id == supplier_id)
        if chantier_id:
            query = query.filter(Purchase.chantier_id == chantier_id)
        if task_id:
            query = query.filter(Purchase.task_id == task_id)
        if is_quick_purchase is not None:
            query = query.filter(Purchase.is_quick_purchase == is_quick_purchase)
        if start_date:
            query = query.filter(Purchase.date >= start_date)
        if end_date:
            query = query.filter(Purchase.date <= end_date)
        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Purchase.reference.ilike(s),
                    Purchase.subject.ilike(s),
                    Purchase.supplier.has(Supplier.name.ilike(s)),
                    Purchase.chantier.has(Chantier.name.ilike(s)),
                )
            )

        total = query.count()
        purchases = query.order_by(Purchase.date.desc(), Purchase.id.desc()).offset(skip).limit(limit).all()
        return purchases, total

    def get_purchase_by_id(self, purchase_id: int) -> Purchase:
        purchase = (
            self.db.query(Purchase)
            .options(
                joinedload(Purchase.supplier),
                joinedload(Purchase.chantier),
                joinedload(Purchase.task),
                joinedload(Purchase.lines).joinedload(PurchaseLine.material).joinedload(Material.unit),
                joinedload(Purchase.receipts).joinedload(PurchaseReceipt.items).joinedload(PurchaseReceiptItem.material),
                joinedload(Purchase.documents),
            )
            .filter(Purchase.id == purchase_id)
            .first()
        )
        if not purchase:
            raise HTTPException(status_code=404, detail="Achat introuvable")
        return purchase

    def create_purchase(self, data: PurchaseCreate, user_id: Optional[int] = None) -> Purchase:
        # Validate Chantier
        chantier = self.db.query(Chantier).filter(Chantier.id == data.chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=400, detail="Chantier spécifié introuvable")

        # Validate Task if provided
        if data.task_id:
            task = self.db.query(Task).filter(Task.id == data.task_id).first()
            if not task:
                raise HTTPException(status_code=400, detail="Tâche spécifiée introuvable")
            if task.chantier_id != data.chantier_id:
                raise HTTPException(status_code=400, detail="La tâche sélectionnée n'appartient pas à ce chantier")

        # Validate Supplier
        supplier = self.db.query(Supplier).filter(Supplier.id == data.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=400, detail="Fournisseur spécifié introuvable")

        reference = data.reference.strip() if data.reference else self.generate_purchase_ref()
        if self.db.query(Purchase).filter(Purchase.reference == reference).first():
            reference = self.generate_purchase_ref()

        purchase = Purchase(
            reference=reference,
            supplier_id=data.supplier_id,
            chantier_id=data.chantier_id,
            task_id=data.task_id,
            date=data.date,
            status=data.status or "Brouillon",
            payment_status=data.payment_status or "Non payé",
            payment_mode=data.payment_mode or "Virement",
            subject=data.subject.strip() if data.subject else None,
            notes=data.notes.strip() if data.notes else None,
            currency=getattr(data, "currency", None) or "FCFA",
            is_quick_purchase=getattr(data, "is_quick_purchase", False) or False,
            total_amount=0.0,
        )
        self.db.add(purchase)
        self.db.flush()

        # Add lines and compute total
        total_amount = 0.0
        for line_data in data.lines:
            mat = self.db.query(Material).filter(Material.id == line_data.material_id).first()
            if not mat:
                raise HTTPException(status_code=400, detail=f"Matériau {line_data.material_id} introuvable")

            total_line_price = getattr(line_data, "total_price", None) or (line_data.quantity * line_data.unit_price)
            line = PurchaseLine(
                purchase_id=purchase.id,
                material_id=line_data.material_id,
                quantity=line_data.quantity,
                unit_price=line_data.unit_price,
                total_price=total_line_price,
                quantity_received=0.0,
            )
            self.db.add(line)
            total_amount += float(total_line_price)

        purchase.total_amount = round(total_amount, 2)
        self.db.commit()
        return self.get_purchase_by_id(purchase.id)

    def quick_purchase(self, data: QuickPurchaseCreate, user_id: Optional[int] = None) -> Purchase:
        """
        Crée un achat rapide (mode terrain/urgence).
        Gère la création dynamique du fournisseur ou du matériau si nécessaire.
        Auto-réceptionne dans le dépôt si auto_receive=True.
        """
        # 1. Fournisseur
        supplier_id = getattr(data, "supplier_id", None)
        supplier_name = getattr(data, "supplier_name", None)
        supplier_phone = getattr(data, "supplier_phone", None)
        if not supplier_id:
            if not supplier_name:
                raise HTTPException(status_code=400, detail="Veuillez indiquer un fournisseur ou son nom")
            # Create quick supplier
            new_sup = Supplier(
                code=self.generate_supplier_code(),
                name=supplier_name.strip(),
                phone=supplier_phone.strip() if supplier_phone else "Non renseigné",
                city="Abidjan",
                country="Côte d'Ivoire",
            )
            self.db.add(new_sup)
            self.db.flush()
            supplier_id = new_sup.id

        # 2. Chantier & Tâche
        chantier = self.db.query(Chantier).filter(Chantier.id == data.chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=400, detail="Chantier spécifié introuvable")

        task_id = getattr(data, "task_id", None)
        if task_id:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task or task.chantier_id != data.chantier_id:
                raise HTTPException(status_code=400, detail="La tâche sélectionnée n'appartient pas à ce chantier")

        # 3. Create Purchase
        auto_receive = getattr(data, "auto_receive", True)
        purchase_ref = self.generate_purchase_ref()
        purchase = Purchase(
            reference=purchase_ref,
            supplier_id=supplier_id,
            chantier_id=data.chantier_id,
            task_id=task_id,
            date=getattr(data, "date", None) or date.today(),
            status="Reçu" if auto_receive else "Commandé",
            payment_status=getattr(data, "payment_status", "Payé") or "Payé",
            payment_mode=getattr(data, "payment_mode", "Espèces") or "Espèces",
            subject=getattr(data, "subject", None) or f"Achat direct terrain - {chantier.name}",
            notes=getattr(data, "notes", None),
            currency="FCFA",
            is_quick_purchase=True,
            total_amount=0.0,
        )
        self.db.add(purchase)
        self.db.flush()

        # 4. Process lines
        total_amount = 0.0
        lines_to_receive = []
        raw_items = getattr(data, "items", None)
        if not raw_items:
            mat_id = getattr(data, "material_id", None)
            mat_name = getattr(data, "material_name", None)
            qty = getattr(data, "quantity", 1.0) or 1.0
            price = getattr(data, "unit_price", 0.0) or 0.0
            if mat_id or mat_name:
                class SimpleItem:
                    def __init__(self, m_id, m_name, q, p):
                        self.material_id = m_id
                        self.material_name = m_name
                        self.quantity = q
                        self.unit_price = p
                raw_items = [SimpleItem(mat_id, mat_name, qty, price)]
            else:
                raw_items = []

        for item in raw_items:
            mat_id = item.material_id
            if not mat_id:
                if not item.material_name:
                    continue
                # Create quick material
                cat = self.db.query(MaterialCategory).first()
                unit = self.db.query(MaterialUnit).first()
                if not cat:
                    cat = MaterialCategory(code="CAT-DIVERS", name="Divers")
                    self.db.add(cat)
                    self.db.flush()
                if not unit:
                    unit = MaterialUnit(code="U", name="Unité")
                    self.db.add(unit)
                    self.db.flush()

                new_mat = Material(
                    code=self.generate_material_code(),
                    name=item.material_name.strip(),
                    category_id=cat.id,
                    unit_id=unit.id,
                    indicative_price=item.unit_price,
                )
                self.db.add(new_mat)
                self.db.flush()
                mat_id = new_mat.id

            total_line = item.quantity * item.unit_price
            line = PurchaseLine(
                purchase_id=purchase.id,
                material_id=mat_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=total_line,
                quantity_received=item.quantity if auto_receive else 0.0,
            )
            self.db.add(line)
            self.db.flush()
            total_amount += total_line
            lines_to_receive.append((line, mat_id, item.quantity, item.unit_price))

        purchase.total_amount = round(total_amount, 2)

        # 5. If auto-receive, generate receipt and stock movement
        if auto_receive and lines_to_receive:
            loc_id = getattr(data, "location_id", None)
            if not loc_id:
                loc = self.db.query(StockLocation).filter(StockLocation.is_active == True).first()
                if not loc:
                    loc = StockLocation(code="DEP-01", name="Dépôt Principal")
                    self.db.add(loc)
                    self.db.flush()
                loc_id = loc.id

            receipt = PurchaseReceipt(
                purchase_id=purchase.id,
                receipt_number=self.generate_receipt_ref(),
                date=getattr(data, "date", None) or date.today(),
                location_id=loc_id,
                notes="Réception automatique - Achat rapide",
            )
            self.db.add(receipt)
            self.db.flush()

            for line_obj, mat_id, qty, u_price in lines_to_receive:
                item_rec = PurchaseReceiptItem(
                    receipt_id=receipt.id,
                    purchase_line_id=line_obj.id,
                    material_id=mat_id,
                    quantity_received=qty,
                    quantity_rejected=0.0,
                )
                self.db.add(item_rec)

                # Stock Movement (Entrée)
                mvt = StockMovement(
                    reference=self.generate_movement_ref(),
                    material_id=mat_id,
                    location_id=loc_id,
                    movement_type="Entrée",
                    quantity=qty,
                    unit_price=u_price,
                    chantier_id=data.chantier_id,
                    task_id=data.task_id,
                    purchase_id=purchase.id,
                    user_id=user_id,
                    date=datetime.utcnow(),
                    reason="Réception achat rapide",
                )
                self.db.add(mvt)

        self.db.commit()
        return self.get_purchase_by_id(purchase.id)

    def update_purchase(self, purchase_id: int, data: PurchaseUpdate) -> Purchase:
        purchase = self.db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            raise HTTPException(status_code=404, detail="Achat introuvable")

        if data.chantier_id is not None:
            c = self.db.query(Chantier).filter(Chantier.id == data.chantier_id).first()
            if not c:
                raise HTTPException(status_code=400, detail="Chantier introuvable")
            purchase.chantier_id = data.chantier_id

        if data.task_id is not None:
            if data.task_id != 0:
                t = self.db.query(Task).filter(Task.id == data.task_id).first()
                if not t or t.chantier_id != purchase.chantier_id:
                    raise HTTPException(status_code=400, detail="La tâche n'appartient pas au chantier sélectionné")
                purchase.task_id = data.task_id
            else:
                purchase.task_id = None

        if data.supplier_id is not None:
            purchase.supplier_id = data.supplier_id
        if data.date is not None:
            purchase.date = data.date
        if data.status is not None:
            purchase.status = data.status
        if data.payment_status is not None:
            purchase.payment_status = data.payment_status
        if data.payment_mode is not None:
            purchase.payment_mode = data.payment_mode
        if data.subject is not None:
            purchase.subject = data.subject
        if data.notes is not None:
            purchase.notes = data.notes

        # If lines provided, replace existing lines
        if data.lines is not None:
            # Delete old lines
            self.db.query(PurchaseLine).filter(PurchaseLine.purchase_id == purchase_id).delete()
            total_amount = 0.0
            for line_data in data.lines:
                total_line = getattr(line_data, "total_price", None) or (line_data.quantity * line_data.unit_price)
                new_line = PurchaseLine(
                    purchase_id=purchase.id,
                    material_id=line_data.material_id,
                    quantity=line_data.quantity,
                    unit_price=line_data.unit_price,
                    total_price=total_line,
                    quantity_received=0.0,
                )
                self.db.add(new_line)
                total_amount += float(total_line)
            purchase.total_amount = round(total_amount, 2)

        self.db.commit()
        return self.get_purchase_by_id(purchase.id)

    def delete_purchase(self, purchase_id: int) -> bool:
        purchase = self.db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            raise HTTPException(status_code=404, detail="Achat introuvable")

        has_receipts = self.db.query(PurchaseReceipt).filter(PurchaseReceipt.purchase_id == purchase_id).first()
        if has_receipts:
            raise HTTPException(status_code=400, detail="Impossible de supprimer un achat ayant déjà des bons de réception enregistrés")

        self.db.delete(purchase)
        self.db.commit()
        return True

    # =========================================================================
    # 7. RÉCEPTIONS D'ACHAT (Purchase Receipts)
    # =========================================================================
    def create_receipt(
        self,
        purchase_id: int,
        data: PurchaseReceiptCreate,
        user_id: Optional[int] = None,
    ) -> PurchaseReceipt:
        purchase = self.get_purchase_by_id(purchase_id)
        location = self.db.query(StockLocation).filter(StockLocation.id == data.location_id).first()
        if not location:
            raise HTTPException(status_code=400, detail="Emplacement de stockage introuvable")

        receipt_number = data.receipt_number.strip() if data.receipt_number else self.generate_receipt_ref()
        if self.db.query(PurchaseReceipt).filter(PurchaseReceipt.receipt_number == receipt_number).first():
            receipt_number = self.generate_receipt_ref()

        receipt = PurchaseReceipt(
            purchase_id=purchase.id,
            receipt_number=receipt_number,
            date=data.date,
            location_id=data.location_id,
            notes=data.notes.strip() if data.notes else None,
        )
        self.db.add(receipt)
        self.db.flush()

        for item in data.items:
            line = self.db.query(PurchaseLine).filter(PurchaseLine.id == item.purchase_line_id).first()
            if not line or line.purchase_id != purchase_id:
                raise HTTPException(status_code=400, detail=f"Ligne d'achat {item.purchase_line_id} invalide")

            # Add receipt item
            rec_item = PurchaseReceiptItem(
                receipt_id=receipt.id,
                purchase_line_id=line.id,
                material_id=line.material_id,
                quantity_received=item.quantity_received,
                quantity_rejected=item.quantity_rejected,
                rejection_reason=item.rejection_reason,
            )
            self.db.add(rec_item)

            # Update line quantity_received
            line.quantity_received += item.quantity_received

            # Automatically create StockMovement (Entrée) for accepted quantity
            if item.quantity_received > 0:
                mvt = StockMovement(
                    reference=self.generate_movement_ref(),
                    material_id=line.material_id,
                    location_id=data.location_id,
                    movement_type="Entrée",
                    quantity=item.quantity_received,
                    unit_price=float(line.unit_price),
                    chantier_id=purchase.chantier_id,
                    task_id=purchase.task_id,
                    purchase_id=purchase.id,
                    user_id=user_id,
                    date=datetime.combine(data.date, datetime.min.time()),
                    reason=f"Réception {receipt_number} (Achat {purchase.reference})",
                )
                self.db.add(mvt)

        # Check overall receipt status for the purchase
        all_lines = self.db.query(PurchaseLine).filter(PurchaseLine.purchase_id == purchase_id).all()
        all_completed = True
        any_received = False
        for l in all_lines:
            if l.quantity_received < l.quantity:
                all_completed = False
            if l.quantity_received > 0:
                any_received = True

        if all_completed:
            purchase.status = "Reçu"
        elif any_received:
            purchase.status = "Partiellement reçu"

        self.db.commit()
        self.db.refresh(receipt)
        return receipt

    # =========================================================================
    # 8. GESTION DU STOCK & MOUVEMENTS (Stock Movements)
    # =========================================================================
    def get_movements(
        self,
        material_id: Optional[int] = None,
        location_id: Optional[int] = None,
        chantier_id: Optional[int] = None,
        task_id: Optional[int] = None,
        movement_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[StockMovement], int]:
        query = (
            self.db.query(StockMovement)
            .options(
                joinedload(StockMovement.material).joinedload(Material.unit),
                joinedload(StockMovement.location),
                joinedload(StockMovement.chantier),
                joinedload(StockMovement.task),
                joinedload(StockMovement.purchase),
                joinedload(StockMovement.user),
            )
        )
        if material_id:
            query = query.filter(StockMovement.material_id == material_id)
        if location_id:
            query = query.filter(StockMovement.location_id == location_id)
        if chantier_id:
            query = query.filter(StockMovement.chantier_id == chantier_id)
        if task_id:
            query = query.filter(StockMovement.task_id == task_id)
        if movement_type:
            query = query.filter(StockMovement.movement_type == movement_type)
        if start_date:
            query = query.filter(StockMovement.date >= start_date)
        if end_date:
            query = query.filter(StockMovement.date <= end_date)

        total = query.count()
        movements = query.order_by(StockMovement.date.desc(), StockMovement.id.desc()).offset(skip).limit(limit).all()
        return movements, total

    def add_direct_movement(
        self,
        data: StockMovementCreate,
        user_id: Optional[int] = None,
    ) -> StockMovement:
        material = self.db.query(Material).filter(Material.id == data.material_id).first()
        if not material:
            raise HTTPException(status_code=400, detail="Matériau introuvable")

        location = self.db.query(StockLocation).filter(StockLocation.id == data.location_id).first()
        if not location:
            raise HTTPException(status_code=400, detail="Emplacement introuvable")

        # If Sortie, check availability
        if data.movement_type.strip().lower() == "sortie":
            curr_stock = self.calculate_material_stock(data.material_id, data.location_id)
            if curr_stock < data.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuffisant au dépôt '{location.name}'. Disponible: {curr_stock}, Demandé: {data.quantity}",
                )

        # Validate chantier and task
        if data.chantier_id:
            ch = self.db.query(Chantier).filter(Chantier.id == data.chantier_id).first()
            if not ch:
                raise HTTPException(status_code=400, detail="Chantier introuvable")
            if data.task_id:
                t = self.db.query(Task).filter(Task.id == data.task_id).first()
                if not t or t.chantier_id != data.chantier_id:
                    raise HTTPException(status_code=400, detail="La tâche sélectionnée n'appartient pas à ce chantier")

        ref = self.generate_movement_ref()
        mvt = StockMovement(
            reference=ref,
            material_id=data.material_id,
            location_id=data.location_id,
            movement_type=data.movement_type,
            quantity=data.quantity,
            unit_price=data.unit_price or float(material.indicative_price or 0.0),
            chantier_id=data.chantier_id,
            task_id=data.task_id,
            purchase_id=data.purchase_id,
            source_location_id=data.source_location_id,
            dest_location_id=data.dest_location_id,
            user_id=user_id,
            date=data.date or datetime.utcnow(),
            reason=data.reason,
            notes=data.notes,
        )
        self.db.add(mvt)
        self.db.commit()
        self.db.refresh(mvt)
        return mvt

    def issue_to_chantier(
        self,
        material_id: int,
        location_id: int,
        chantier_id: int,
        quantity: float,
        task_id: Optional[int] = None,
        reason: Optional[str] = None,
        notes: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> StockMovement:
        """Sortie de stock vers un chantier et éventuellement une tâche spécifique."""
        curr_stock = self.calculate_material_stock(material_id, location_id)
        if curr_stock < quantity:
            loc = self.db.query(StockLocation).filter(StockLocation.id == location_id).first()
            loc_name = loc.name if loc else f"#{location_id}"
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuffisant dans '{loc_name}'. Disponible: {curr_stock}, Demandé: {quantity}",
            )

        data = StockMovementCreate(
            material_id=material_id,
            location_id=location_id,
            movement_type="Sortie",
            quantity=quantity,
            chantier_id=chantier_id,
            task_id=task_id,
            reason=reason or "Affectation sur chantier",
            notes=notes,
        )
        return self.add_direct_movement(data, user_id=user_id)

    def transfer_stock(
        self,
        data: StockTransferCreate,
        user_id: Optional[int] = None,
    ) -> Tuple[StockMovement, StockMovement]:
        """Transfert de stock entre deux dépôts."""
        if data.source_location_id == data.dest_location_id:
            raise HTTPException(status_code=400, detail="L'emplacement source et destination doivent être différents")

        curr_stock = self.calculate_material_stock(data.material_id, data.source_location_id)
        if curr_stock < data.quantity:
            src_loc = self.db.query(StockLocation).filter(StockLocation.id == data.source_location_id).first()
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuffisant au dépôt source '{src_loc.name if src_loc else ''}'. Disponible: {curr_stock}, Demandé: {data.quantity}",
            )

        mat = self.db.query(Material).filter(Material.id == data.material_id).first()
        u_price = float(mat.indicative_price or 0.0) if mat else 0.0

        # Sortie from source
        out_ref = self.generate_movement_ref()
        mvt_out = StockMovement(
            reference=out_ref,
            material_id=data.material_id,
            location_id=data.source_location_id,
            movement_type="Sortie",
            quantity=data.quantity,
            unit_price=u_price,
            source_location_id=data.source_location_id,
            dest_location_id=data.dest_location_id,
            user_id=user_id,
            date=datetime.utcnow(),
            reason=f"Transfert vers dépôt #{data.dest_location_id}: {data.reason or ''}",
            notes=data.notes,
        )
        self.db.add(mvt_out)
        self.db.flush()

        # Entrée to destination
        in_ref = self.generate_movement_ref()
        mvt_in = StockMovement(
            reference=in_ref,
            material_id=data.material_id,
            location_id=data.dest_location_id,
            movement_type="Entrée",
            quantity=data.quantity,
            unit_price=u_price,
            source_location_id=data.source_location_id,
            dest_location_id=data.dest_location_id,
            user_id=user_id,
            date=datetime.utcnow(),
            reason=f"Transfert depuis dépôt #{data.source_location_id}: {data.reason or ''}",
            notes=data.notes,
        )
        self.db.add(mvt_in)
        self.db.commit()
        return mvt_out, mvt_in

    def return_from_chantier(
        self,
        data: StockReturnCreate,
        user_id: Optional[int] = None,
    ) -> StockMovement:
        """Retour de matériaux non utilisés du chantier vers un dépôt."""
        mat = self.db.query(Material).filter(Material.id == data.material_id).first()
        u_price = float(mat.indicative_price or 0.0) if mat else 0.0

        mvt = StockMovement(
            reference=self.generate_movement_ref(),
            material_id=data.material_id,
            location_id=data.location_id,
            movement_type="Retour",
            quantity=data.quantity,
            unit_price=u_price,
            chantier_id=data.chantier_id,
            user_id=user_id,
            date=datetime.utcnow(),
            reason=data.reason or "Retour matériel non consommé",
            notes=data.notes,
        )
        self.db.add(mvt)
        self.db.commit()
        self.db.refresh(mvt)
        return mvt

    def get_stock_by_locations(self, location_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Donne la répartition du stock par matériau et par emplacement."""
        materials = self.db.query(Material).options(
            joinedload(Material.category),
            joinedload(Material.unit),
        ).filter(Material.is_active == True).all()

        locations_query = self.db.query(StockLocation).filter(StockLocation.is_active == True)
        if location_id:
            locations_query = locations_query.filter(StockLocation.id == location_id)
        locations = locations_query.all()

        results = []
        for loc in locations:
            for mat in materials:
                stock_qty = self.calculate_material_stock(mat.id, loc.id)
                if stock_qty > 0 or not location_id: # include non-zero or all if specific location requested
                    status = "Normal"
                    if stock_qty <= 0:
                        status = "Rupture"
                    elif mat.minimum_stock > 0 and stock_qty <= mat.minimum_stock:
                        status = "Stock faible"

                    results.append({
                        "material_id": mat.id,
                        "material_code": mat.code,
                        "material_name": mat.name,
                        "category_name": mat.category.name if mat.category else "-",
                        "unit_code": mat.unit.code if mat.unit else "U",
                        "location_id": loc.id,
                        "location_name": loc.name,
                        "quantity": stock_qty,
                        "indicative_price": float(mat.indicative_price or 0.0),
                        "stock_value": round(stock_qty * float(mat.indicative_price or 0.0), 2),
                        "minimum_stock": mat.minimum_stock,
                        "stock_status": status,
                    })

        return results

    # =========================================================================
    # 9. INVENTAIRES PHYSIQUES (Physical Inventories)
    # =========================================================================
    def get_inventories(
        self,
        location_id: Optional[int] = None,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[StockInventory], int]:
        query = (
            self.db.query(StockInventory)
            .options(
                joinedload(StockInventory.location),
                joinedload(StockInventory.user),
                joinedload(StockInventory.items).joinedload(StockInventoryItem.material).joinedload(Material.unit),
            )
        )
        if location_id:
            query = query.filter(StockInventory.location_id == location_id)
        if status_filter:
            query = query.filter(StockInventory.status == status_filter)

        total = query.count()
        inventories = query.order_by(StockInventory.inventory_date.desc(), StockInventory.id.desc()).offset(skip).limit(limit).all()
        return inventories, total

    def get_inventory_by_id(self, inventory_id: int) -> StockInventory:
        inv = (
            self.db.query(StockInventory)
            .options(
                joinedload(StockInventory.location),
                joinedload(StockInventory.user),
                joinedload(StockInventory.items).joinedload(StockInventoryItem.material).joinedload(Material.unit),
            )
            .filter(StockInventory.id == inventory_id)
            .first()
        )
        if not inv:
            raise HTTPException(status_code=404, detail="Inventaire introuvable")
        return inv

    def create_inventory(self, data: StockInventoryCreate, user_id: Optional[int] = None) -> StockInventory:
        location = self.db.query(StockLocation).filter(StockLocation.id == data.location_id).first()
        if not location:
            raise HTTPException(status_code=400, detail="Emplacement introuvable")

        ref = self.generate_inventory_ref()
        inv = StockInventory(
            reference=ref,
            location_id=data.location_id,
            inventory_date=data.inventory_date,
            status="Brouillon",
            notes=data.notes,
            created_by=user_id,
        )
        self.db.add(inv)
        self.db.flush()

        # If items provided, add them; otherwise populate automatically with all active materials
        if data.items:
            for item in data.items:
                theo = self.calculate_material_stock(item.material_id, data.location_id)
                actual = item.actual_quantity
                diff = actual - theo
                inv_item = StockInventoryItem(
                    inventory_id=inv.id,
                    material_id=item.material_id,
                    theoretical_quantity=theo,
                    actual_quantity=actual,
                    discrepancy=diff,
                    unit_price=item.unit_price,
                    notes=item.notes,
                )
                self.db.add(inv_item)
        else:
            materials = self.db.query(Material).filter(Material.is_active == True).all()
            for mat in materials:
                theo = self.calculate_material_stock(mat.id, data.location_id)
                inv_item = StockInventoryItem(
                    inventory_id=inv.id,
                    material_id=mat.id,
                    theoretical_quantity=theo,
                    actual_quantity=theo, # default same until counted
                    discrepancy=0.0,
                    unit_price=float(mat.indicative_price or 0.0),
                )
                self.db.add(inv_item)

        self.db.commit()
        return self.get_inventory_by_id(inv.id)

    def validate_inventory(self, inventory_id: int, user_id: Optional[int] = None) -> StockInventory:
        """
        Valide l'inventaire et génère les mouvements d'ajustement nécessaires pour chaque écart constaté.
        """
        inv = self.get_inventory_by_id(inventory_id)
        if inv.status == "Validé":
            raise HTTPException(status_code=400, detail="Cet inventaire est déjà validé")

        for item in inv.items:
            if item.discrepancy != 0:
                # Adjustment movement
                mvt = StockMovement(
                    reference=self.generate_movement_ref(),
                    material_id=item.material_id,
                    location_id=inv.location_id,
                    movement_type="Ajustement",
                    quantity=item.discrepancy, # positive or negative
                    unit_price=float(item.unit_price or 0.0),
                    user_id=user_id,
                    date=datetime.utcnow(),
                    reason=f"Ajustement Inventaire {inv.reference} (écart: {item.discrepancy:+})",
                    notes=item.notes,
                )
                self.db.add(mvt)

        inv.status = "Validé"
        self.db.commit()
        return self.get_inventory_by_id(inv.id)

    # =========================================================================
    # 10. GESTION DES DOCUMENTS & PIÈCES JOINTES (Uploads)
    # =========================================================================
    def upload_document(
        self,
        purchase_id: int,
        file: UploadFile,
        document_type: str,
        document_number: Optional[str] = None,
        document_date: Optional[date] = None,
        user_id: Optional[int] = None,
    ) -> PurchaseDocument:
        purchase = self.get_purchase_by_id(purchase_id)

        target_dir = os.path.join(UPLOAD_DIR, str(purchase_id))
        os.makedirs(target_dir, exist_ok=True)

        original_filename = file.filename or "piece_jointe"
        clean_filename = re.sub(r"[^\w\.-]", "_", original_filename)
        unique_filename = f"{uuid.uuid4().hex[:8]}_{clean_filename}"
        full_path = os.path.join(target_dir, unique_filename)

        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(full_path)

        doc = PurchaseDocument(
            purchase_id=purchase.id,
            document_type=document_type,
            document_number=document_number,
            document_date=document_date or date.today(),
            original_filename=original_filename,
            file_path=full_path,
            mime_type=file.content_type,
            file_size=file_size,
            uploaded_by=user_id,
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def delete_document(self, document_id: int) -> bool:
        doc = self.db.query(PurchaseDocument).filter(PurchaseDocument.id == document_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document introuvable")

        if os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except OSError:
                pass

        self.db.delete(doc)
        self.db.commit()
        return True

    # =========================================================================
    # 11. TABLEAUX DE BORD & ANALYTIQUES
    # =========================================================================
    def get_purchases_dashboard(self) -> Dict[str, Any]:
        purchases = self.db.query(Purchase).all()
        total_purchases = len(purchases)
        pending = sum(1 for p in purchases if p.status in ["Brouillon", "En attente"])
        ordered = sum(1 for p in purchases if p.status == "Commandé")
        partially = sum(1 for p in purchases if p.status == "Partiellement reçu")
        received = sum(1 for p in purchases if p.status == "Reçu")

        total_committed = sum(float(p.total_amount) for p in purchases if p.status != "Annulé")
        total_paid = sum(float(p.total_amount) for p in purchases if p.payment_status == "Payé" and p.status != "Annulé")
        total_paid += sum(float(p.total_amount) * 0.5 for p in purchases if p.payment_status == "Partiellement payé" and p.status != "Annulé")
        remaining = total_committed - total_paid

        return {
            "total_purchases": total_purchases,
            "pending_purchases": pending,
            "ordered_purchases": ordered,
            "partially_received_purchases": partially,
            "received_purchases": received,
            "total_committed_amount": round(total_committed, 2),
            "total_paid_amount": round(total_paid, 2),
            "remaining_to_pay": round(max(0.0, remaining), 2),
        }

    def get_stock_dashboard(self) -> Dict[str, Any]:
        materials, total_materials = self.get_materials(limit=1000)
        locations = self.db.query(StockLocation).filter(StockLocation.is_active == True).all()

        active_count = sum(1 for m in materials if m["is_active"])
        out_of_stock = sum(1 for m in materials if m["stock_status"] == "Rupture")
        low_stock = sum(1 for m in materials if m["stock_status"] == "Stock faible")
        total_value = sum(m["stock_value"] for m in materials)

        alerts = [m for m in materials if m["stock_status"] in ["Rupture", "Stock faible"]]

        return {
            "total_materials_count": total_materials,
            "active_materials_count": active_count,
            "out_of_stock_count": out_of_stock,
            "low_stock_count": low_stock,
            "total_stock_value": round(total_value, 2),
            "total_locations_count": len(locations),
            "alerts": alerts[:10],
        }

    def get_chantier_consumption(self, chantier_id: int) -> Dict[str, Any]:
        chantier = self.db.query(Chantier).filter(Chantier.id == chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=404, detail="Chantier introuvable")

        purchases = self.db.query(Purchase).filter(
            Purchase.chantier_id == chantier_id,
            Purchase.status != "Annulé",
        ).all()

        total_purchases = sum(float(p.total_amount) for p in purchases)
        total_paid = sum(float(p.total_amount) for p in purchases if p.payment_status == "Payé")
        total_paid += sum(float(p.total_amount) * 0.5 for p in purchases if p.payment_status == "Partiellement payé")
        remaining = total_purchases - total_paid

        # Materials ordered via purchases
        mat_ordered_map = {}
        for p in purchases:
            for l in p.lines:
                mid = l.material_id
                if mid not in mat_ordered_map:
                    mat_ordered_map[mid] = {
                        "material_id": mid,
                        "material_code": l.material.code,
                        "material_name": l.material.name,
                        "unit": l.material.unit.code if l.material.unit else "U",
                        "quantity_ordered": 0.0,
                        "quantity_received": 0.0,
                        "total_amount": 0.0,
                    }
                mat_ordered_map[mid]["quantity_ordered"] += float(l.quantity)
                mat_ordered_map[mid]["quantity_received"] += float(l.quantity_received)
                mat_ordered_map[mid]["total_amount"] += float(l.total_price)

        # Materials issued to this chantier
        issued_mvts = self.db.query(StockMovement).filter(
            StockMovement.chantier_id == chantier_id,
            StockMovement.movement_type == "Sortie",
        ).all()

        mat_issued_map = {}
        for m in issued_mvts:
            mid = m.material_id
            if mid not in mat_issued_map:
                mat_issued_map[mid] = {
                    "material_id": mid,
                    "material_code": m.material.code,
                    "material_name": m.material.name,
                    "unit": m.material.unit.code if m.material.unit else "U",
                    "quantity_issued": 0.0,
                    "total_cost": 0.0,
                }
            mat_issued_map[mid]["quantity_issued"] += float(m.quantity)
            mat_issued_map[mid]["total_cost"] += float(m.quantity) * float(m.unit_price or 0.0)

        return {
            "chantier_id": chantier.id,
            "chantier_code": chantier.code,
            "chantier_name": chantier.name,
            "total_purchases_amount": round(total_purchases, 2),
            "total_paid_amount": round(total_paid, 2),
            "remaining_to_pay": round(max(0.0, remaining), 2),
            "materials_ordered": list(mat_ordered_map.values()),
            "materials_issued": list(mat_issued_map.values()),
        }
