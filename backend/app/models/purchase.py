from typing import Optional, List
from datetime import date, datetime
from sqlalchemy import (
    String,
    Boolean,
    Text,
    Float,
    Integer,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: FOUR-001
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Raison sociale
    trade_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Nom commercial
    contact_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), default="Abidjan", nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="Côte d'Ivoire", nullable=False)

    # Informations administratives
    rccm: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ncc: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Conditions commerciales
    payment_terms: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relations
    purchases: Mapped[List["Purchase"]] = relationship("Purchase", back_populates="supplier")

    def __repr__(self) -> str:
        return f"<Supplier id={self.id} code='{self.code}' name='{self.name}'>"


class MaterialCategory(Base, TimestampMixin):
    __tablename__ = "material_categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: CAT-CIMENT
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    materials: Mapped[List["Material"]] = relationship("Material", back_populates="category")

    def __repr__(self) -> str:
        return f"<MaterialCategory id={self.id} name='{self.name}'>"


class MaterialUnit(Base, TimestampMixin):
    __tablename__ = "material_units"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False) # Ex: SAC, T, BARRE, M3, U
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False) # Ex: Sac, Tonne, Barre, Mètre cube

    materials: Mapped[List["Material"]] = relationship("Material", back_populates="unit")

    def __repr__(self) -> str:
        return f"<MaterialUnit id={self.id} code='{self.code}' name='{self.name}'>"


class Material(Base, TimestampMixin):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: MAT-2026-001
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Ex: Ciment CPJ 35
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("material_categories.id", ondelete="RESTRICT"), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("material_units.id", ondelete="RESTRICT"), nullable=False)

    reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # Référence catalogue
    indicative_price: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    minimum_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    maximum_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relations
    category: Mapped[MaterialCategory] = relationship("MaterialCategory", back_populates="materials")
    unit: Mapped[MaterialUnit] = relationship("MaterialUnit", back_populates="materials")
    purchase_lines: Mapped[List["PurchaseLine"]] = relationship("PurchaseLine", back_populates="material")
    stock_movements: Mapped[List["StockMovement"]] = relationship("StockMovement", back_populates="material")

    def __repr__(self) -> str:
        return f"<Material id={self.id} code='{self.code}' name='{self.name}'>"


class StockLocation(Base, TimestampMixin):
    __tablename__ = "stock_locations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: DEP-01
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False) # Ex: Dépôt principal Yopougon
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(50), default="Dépôt principal", nullable=False) # Dépôt principal, Magasin, Entrepôt
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<StockLocation id={self.id} code='{self.code}' name='{self.name}'>"


class Purchase(Base, TimestampMixin):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: ACH-2026-00001

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id", ondelete="RESTRICT"), index=True, nullable=False)
    chantier_id: Mapped[int] = mapped_column(ForeignKey("chantiers.id", ondelete="CASCADE"), index=True, nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True, nullable=True)

    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Brouillon", nullable=False) # Brouillon, En attente, Validé, Commandé, Partiellement reçu, Reçu, Annulé, Clôturé
    payment_status: Mapped[str] = mapped_column(String(50), default="Non payé", nullable=False) # Non payé, Partiellement payé, Payé
    payment_mode: Mapped[Optional[str]] = mapped_column(String(50), default="Virement", nullable=True) # Espèces, Virement, Chèque, Mobile Money

    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Objet de l'achat
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_amount: Mapped[float] = mapped_column(Numeric(15, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="FCFA", nullable=False)
    is_quick_purchase: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relations
    supplier: Mapped[Supplier] = relationship("Supplier", back_populates="purchases")
    chantier: Mapped["Chantier"] = relationship("Chantier")
    task: Mapped[Optional["Task"]] = relationship("Task")

    lines: Mapped[List["PurchaseLine"]] = relationship(
        "PurchaseLine",
        back_populates="purchase",
        cascade="all, delete-orphan",
    )
    receipts: Mapped[List["PurchaseReceipt"]] = relationship(
        "PurchaseReceipt",
        back_populates="purchase",
        cascade="all, delete-orphan",
    )
    documents: Mapped[List["PurchaseDocument"]] = relationship(
        "PurchaseDocument",
        back_populates="purchase",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Purchase id={self.id} reference='{self.reference}' total={self.total_amount}>"

    @property
    def reception_percentage(self) -> float:
        if not self.lines:
            return 0.0
        total_ordered = sum(float(line.quantity) for line in self.lines)
        if total_ordered <= 0:
            return 0.0
        total_received = sum(float(line.quantity_received) for line in self.lines)
        return min(100.0, round((total_received / total_ordered) * 100, 1))

    @property
    def documents_count(self) -> int:
        return len(self.documents) if self.documents else 0

    @property
    def supplier_name(self) -> Optional[str]:
        return self.supplier.name if self.supplier else None

    @property
    def chantier_name(self) -> Optional[str]:
        return self.chantier.name if self.chantier else None

    @property
    def chantier_code(self) -> Optional[str]:
        return getattr(self.chantier, "code", None) if self.chantier else None

    @property
    def task_name(self) -> Optional[str]:
        return self.task.name if self.task else None

    @property
    def task_code(self) -> Optional[str]:
        return getattr(self.task, "code", None) if self.task else None


class PurchaseLine(Base, TimestampMixin):
    __tablename__ = "purchase_lines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id", ondelete="CASCADE"), index=True, nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id", ondelete="RESTRICT"), index=True, nullable=False)

    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    quantity_received: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relations
    purchase: Mapped[Purchase] = relationship("Purchase", back_populates="lines")
    material: Mapped[Material] = relationship("Material", back_populates="purchase_lines")

    def __repr__(self) -> str:
        return f"<PurchaseLine id={self.id} purchase_id={self.purchase_id} qty={self.quantity}>"

    @property
    def material_code(self) -> Optional[str]:
        return self.material.code if self.material else None

    @property
    def material_name(self) -> Optional[str]:
        return self.material.name if self.material else None

    @property
    def unit_code(self) -> Optional[str]:
        return self.material.unit.code if self.material and self.material.unit else None


class PurchaseReceipt(Base, TimestampMixin):
    __tablename__ = "purchase_receipts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id", ondelete="CASCADE"), index=True, nullable=False)
    receipt_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: REC-2026-00001
    date: Mapped[date] = mapped_column(Date, nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("stock_locations.id", ondelete="RESTRICT"), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relations
    purchase: Mapped[Purchase] = relationship("Purchase", back_populates="receipts")
    location: Mapped[StockLocation] = relationship("StockLocation")
    items: Mapped[List["PurchaseReceiptItem"]] = relationship(
        "PurchaseReceiptItem",
        back_populates="receipt",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PurchaseReceipt id={self.id} number='{self.receipt_number}'>"

    @property
    def location_name(self) -> Optional[str]:
        return self.location.name if self.location else None


class PurchaseReceiptItem(Base):
    __tablename__ = "purchase_receipt_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("purchase_receipts.id", ondelete="CASCADE"), index=True, nullable=False)
    purchase_line_id: Mapped[int] = mapped_column(ForeignKey("purchase_lines.id", ondelete="CASCADE"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id", ondelete="RESTRICT"), nullable=False)

    quantity_received: Mapped[float] = mapped_column(Float, nullable=False)
    quantity_rejected: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relations
    receipt: Mapped[PurchaseReceipt] = relationship("PurchaseReceipt", back_populates="items")
    purchase_line: Mapped[PurchaseLine] = relationship("PurchaseLine")
    material: Mapped[Material] = relationship("Material")

    def __repr__(self) -> str:
        return f"<PurchaseReceiptItem id={self.id} received={self.quantity_received}>"

    @property
    def material_name(self) -> Optional[str]:
        return self.material.name if self.material else None

    @property
    def unit_code(self) -> Optional[str]:
        return self.material.unit.code if self.material and self.material.unit else None


class StockMovement(Base, TimestampMixin):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: MVT-2026-00001
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id", ondelete="RESTRICT"), index=True, nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("stock_locations.id", ondelete="RESTRICT"), index=True, nullable=False)

    movement_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # Entrée, Sortie, Transfert, Retour, Ajustement, Inventaire
    quantity: Mapped[float] = mapped_column(Float, nullable=False) # Positif pour entrée/retour, négatif pour sortie
    unit_price: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)

    chantier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chantiers.id", ondelete="SET NULL"), index=True, nullable=True)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True, nullable=True)
    purchase_id: Mapped[Optional[int]] = mapped_column(ForeignKey("purchases.id", ondelete="SET NULL"), index=True, nullable=True)

    source_location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stock_locations.id", ondelete="SET NULL"), nullable=True)
    dest_location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stock_locations.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relations
    material: Mapped[Material] = relationship("Material", back_populates="stock_movements")
    location: Mapped[StockLocation] = relationship("StockLocation", foreign_keys=[location_id])
    chantier: Mapped[Optional["Chantier"]] = relationship("Chantier")
    task: Mapped[Optional["Task"]] = relationship("Task")
    purchase: Mapped[Optional[Purchase]] = relationship("Purchase")
    user: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<StockMovement id={self.id} type='{self.movement_type}' qty={self.quantity}>"


class StockInventory(Base, TimestampMixin):
    __tablename__ = "stock_inventories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: INV-2026-001
    location_id: Mapped[int] = mapped_column(ForeignKey("stock_locations.id", ondelete="RESTRICT"), nullable=False)
    inventory_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Brouillon", nullable=False) # Brouillon, Validé, Annulé
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relations
    location: Mapped[StockLocation] = relationship("StockLocation")
    user: Mapped[Optional["User"]] = relationship("User")
    items: Mapped[List["StockInventoryItem"]] = relationship(
        "StockInventoryItem",
        back_populates="inventory",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<StockInventory id={self.id} ref='{self.reference}'>"


class StockInventoryItem(Base):
    __tablename__ = "stock_inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    inventory_id: Mapped[int] = mapped_column(ForeignKey("stock_inventories.id", ondelete="CASCADE"), index=True, nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id", ondelete="RESTRICT"), nullable=False)

    theoretical_quantity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    actual_quantity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    discrepancy: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # actual - theoretical
    unit_price: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relations
    inventory: Mapped[StockInventory] = relationship("StockInventory", back_populates="items")
    material: Mapped[Material] = relationship("Material")

    def __repr__(self) -> str:
        return f"<StockInventoryItem id={self.id} mat={self.material_id} diff={self.discrepancy}>"


class PurchaseDocument(Base, TimestampMixin):
    __tablename__ = "purchase_documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id", ondelete="CASCADE"), index=True, nullable=False)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False) # Devis, Bon de commande, Bon de livraison, Facture, Reçu, Justificatif de paiement, Photo de livraison, Photo de matériau, Autre
    document_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    document_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    uploaded_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relations
    purchase: Mapped[Purchase] = relationship("Purchase", back_populates="documents")
    uploader: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<PurchaseDocument id={self.id} type='{self.document_type}' filename='{self.original_filename}'>"
