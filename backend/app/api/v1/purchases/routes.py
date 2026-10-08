import os
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, status, Query, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.purchase import PurchaseService
from app.schemas.purchase import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
    SupplierStatsResponse,
    MaterialCategoryCreate,
    MaterialCategoryUpdate,
    MaterialCategoryResponse,
    MaterialUnitCreate,
    MaterialUnitUpdate,
    MaterialUnitResponse,
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse,
    StockLocationCreate,
    StockLocationUpdate,
    StockLocationResponse,
    PurchaseCreate,
    PurchaseUpdate,
    PurchaseResponse,
    PurchaseDetailResponse,
    QuickPurchaseCreate,
    PurchaseReceiptCreate,
    PurchaseReceiptResponse,
    StockMovementCreate,
    StockTransferCreate,
    StockReturnCreate,
    StockMovementResponse,
    StockInventoryCreate,
    StockInventoryResponse,
    PurchaseDocumentResponse,
    PurchaseDashboardResponse,
    StockDashboardResponse,
    MaterialStockAtLocation,
    ChantierConsumptionResponse,
)

router = APIRouter(
    prefix="",
    tags=["Achats, Fournisseurs, Matériaux & Stocks"],
)


# =============================================================================
# 1. FOURNISSEURS (Suppliers)
# =============================================================================
@router.get("/suppliers", response_model=List[SupplierResponse], summary="Lister les fournisseurs")
def list_suppliers(
    search: Optional[str] = Query(None, description="Recherche par nom, code, tél, email"),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    suppliers, _ = service.get_suppliers(search=search, is_active=is_active, skip=skip, limit=limit)
    return suppliers


@router.post("/suppliers", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED, summary="Créer un fournisseur")
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_supplier(data)


@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse, summary="Détail d'un fournisseur")
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_supplier_by_id(supplier_id)


@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse, summary="Modifier un fournisseur")
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.update_supplier(supplier_id, data)


@router.delete("/suppliers/{supplier_id}", summary="Supprimer ou désactiver un fournisseur")
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_supplier(supplier_id)
    return {"detail": "Fournisseur supprimé ou désactivé avec succès"}


@router.get("/suppliers/{supplier_id}/stats", response_model=SupplierStatsResponse, summary="Statistiques financières du fournisseur")
def get_supplier_stats(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_supplier_stats(supplier_id)


# =============================================================================
# 2. CATÉGORIES & UNITÉS DE MATÉRIAUX
# =============================================================================
@router.get("/materials/categories", response_model=List[MaterialCategoryResponse], summary="Lister les catégories de matériaux")
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_categories()


@router.post("/materials/categories", response_model=MaterialCategoryResponse, status_code=status.HTTP_201_CREATED, summary="Créer une catégorie")
def create_category(
    data: MaterialCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_category(data)


@router.put("/materials/categories/{category_id}", response_model=MaterialCategoryResponse, summary="Modifier une catégorie")
def update_category(
    category_id: int,
    data: MaterialCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.update_category(category_id, data)


@router.delete("/materials/categories/{category_id}", summary="Supprimer une catégorie")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_category(category_id)
    return {"detail": "Catégorie supprimée"}


@router.get("/materials/units", response_model=List[MaterialUnitResponse], summary="Lister les unités de mesure")
def list_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_units()


@router.post("/materials/units", response_model=MaterialUnitResponse, status_code=status.HTTP_201_CREATED, summary="Créer une unité")
def create_unit(
    data: MaterialUnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_unit(data)


@router.put("/materials/units/{unit_id}", response_model=MaterialUnitResponse, summary="Modifier une unité")
def update_unit(
    unit_id: int,
    data: MaterialUnitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.update_unit(unit_id, data)


@router.delete("/materials/units/{unit_id}", summary="Supprimer une unité")
def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_unit(unit_id)
    return {"detail": "Unité supprimée"}


# =============================================================================
# 3. MATÉRIAUX (Materials)
# =============================================================================
@router.get("/materials", response_model=List[MaterialResponse], summary="Lister les matériaux avec stock en temps réel")
def list_materials(
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    stock_status: Optional[str] = Query(None, description="Filtre: Rupture, Stock faible, Normal, Surstock"),
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    materials, _ = service.get_materials(
        category_id=category_id,
        search=search,
        is_active=is_active,
        stock_status_filter=stock_status,
        skip=skip,
        limit=limit,
    )
    return materials


@router.post("/materials", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED, summary="Créer un matériau")
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_material(data)


@router.get("/materials/{material_id}", response_model=MaterialResponse, summary="Détail d'un matériau avec stock")
def get_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_material_by_id(material_id)


@router.put("/materials/{material_id}", response_model=MaterialResponse, summary="Modifier un matériau")
def update_material(
    material_id: int,
    data: MaterialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.update_material(material_id, data)


@router.delete("/materials/{material_id}", summary="Supprimer ou désactiver un matériau")
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_material(material_id)
    return {"detail": "Matériau supprimé ou archivé"}


# =============================================================================
# 4. EMPLACEMENTS DE STOCK / DÉPÔTS (Stock Locations)
# =============================================================================
@router.get("/stocks/locations", response_model=List[StockLocationResponse], summary="Lister les dépôts / magasins")
def list_locations(
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_locations(is_active=is_active)


@router.post("/stocks/locations", response_model=StockLocationResponse, status_code=status.HTTP_201_CREATED, summary="Créer un dépôt / magasin")
def create_location(
    data: StockLocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_location(data)


@router.put("/stocks/locations/{location_id}", response_model=StockLocationResponse, summary="Modifier un dépôt")
def update_location(
    location_id: int,
    data: StockLocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.update_location(location_id, data)


@router.delete("/stocks/locations/{location_id}", summary="Supprimer ou désactiver un dépôt")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_location(location_id)
    return {"detail": "Emplacement supprimé ou désactivé"}


# =============================================================================
# 5. ACHATS (Purchases)
# =============================================================================
@router.get("/purchases", response_model=List[PurchaseResponse], summary="Lister les achats / commandes")
def list_purchases(
    status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    supplier_id: Optional[int] = Query(None),
    chantier_id: Optional[int] = Query(None),
    task_id: Optional[int] = Query(None),
    is_quick_purchase: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchases, _ = service.get_purchases(
        status_filter=status,
        payment_status=payment_status,
        supplier_id=supplier_id,
        chantier_id=chantier_id,
        task_id=task_id,
        is_quick_purchase=is_quick_purchase,
        search=search,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return purchases


@router.post("/purchases", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED, summary="Créer un achat standard")
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_purchase(data, user_id=current_user.id)


@router.post("/purchases/quick", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED, summary="Créer un achat rapide terrain")
def create_quick_purchase(
    data: QuickPurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.quick_purchase(data, user_id=current_user.id)


@router.get("/purchases/{purchase_id}", response_model=PurchaseDetailResponse, summary="Détail complet d'un achat")
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_purchase_by_id(purchase_id)


@router.put("/purchases/{purchase_id}", response_model=PurchaseResponse, summary="Modifier un achat")
def update_purchase(
    purchase_id: int,
    data: PurchaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.update_purchase(purchase_id, data)


@router.delete("/purchases/{purchase_id}", summary="Supprimer un achat sans réception")
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_purchase(purchase_id)
    return {"detail": "Achat supprimé avec succès"}


@router.post("/purchases/{purchase_id}/receipts", response_model=PurchaseReceiptResponse, status_code=status.HTTP_201_CREATED, summary="Enregistrer une réception de commande")
def create_receipt(
    purchase_id: int,
    data: PurchaseReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_receipt(purchase_id, data, user_id=current_user.id)


@router.post("/purchases/{purchase_id}/documents", response_model=PurchaseDocumentResponse, status_code=status.HTTP_201_CREATED, summary="Ajouter une pièce jointe à un achat")
def upload_purchase_document(
    purchase_id: int,
    file: UploadFile = File(...),
    document_type: str = Form(..., description="Facture, BL, Bon de commande, Devis, Reçu, Photo..."),
    document_number: Optional[str] = Form(None),
    document_date: Optional[date] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.upload_document(
        purchase_id=purchase_id,
        file=file,
        document_type=document_type,
        document_number=document_number,
        document_date=document_date,
        user_id=current_user.id,
    )


@router.delete("/purchases/documents/{document_id}", summary="Supprimer une pièce jointe")
def delete_purchase_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    service.delete_document(document_id)
    return {"detail": "Document supprimé"}


# =============================================================================
# 6. STOCK & MOUVEMENTS (Stock & Movements)
# =============================================================================
@router.get("/stocks/overview", response_model=List[MaterialStockAtLocation], summary="Vue globale des stocks par dépôt et matériau")
def get_stocks_overview(
    location_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_stock_by_locations(location_id=location_id)


@router.get("/stocks/movements", response_model=List[StockMovementResponse], summary="Historique & Journal des mouvements de stock")
def list_stock_movements(
    material_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    chantier_id: Optional[int] = Query(None),
    task_id: Optional[int] = Query(None),
    movement_type: Optional[str] = Query(None, description="Entrée, Sortie, Transfert, Retour, Ajustement"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    movements, _ = service.get_movements(
        material_id=material_id,
        location_id=location_id,
        chantier_id=chantier_id,
        task_id=task_id,
        movement_type=movement_type,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return movements


@router.post("/stocks/movements", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED, summary="Enregistrer un mouvement de stock direct")
def create_stock_movement(
    data: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.add_direct_movement(data, user_id=current_user.id)


@router.post("/stocks/issue", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED, summary="Sortie de stock vers un chantier / tâche")
def issue_stock_to_chantier(
    material_id: int = Query(..., description="ID du matériau"),
    location_id: int = Query(..., description="Dépôt source"),
    chantier_id: int = Query(..., description="Chantier destinataire"),
    quantity: float = Query(..., gt=0, description="Quantité à sortir"),
    task_id: Optional[int] = Query(None, description="Tâche spécifique du chantier (optionnel)"),
    reason: Optional[str] = Query(None),
    notes: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.issue_to_chantier(
        material_id=material_id,
        location_id=location_id,
        chantier_id=chantier_id,
        quantity=quantity,
        task_id=task_id,
        reason=reason,
        notes=notes,
        user_id=current_user.id,
    )


@router.post("/stocks/transfer", summary="Transfert de stock entre deux dépôts")
def transfer_stock(
    data: StockTransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    out_mvt, in_mvt = service.transfer_stock(data, user_id=current_user.id)
    return {
        "detail": "Transfert effectué avec succès",
        "movement_out_id": out_mvt.id,
        "movement_in_id": in_mvt.id,
    }


@router.post("/stocks/return", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED, summary="Retour matériel chantier vers dépôt")
def return_from_chantier(
    data: StockReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.return_from_chantier(data, user_id=current_user.id)


# =============================================================================
# 7. INVENTAIRES PHYSIQUES (Physical Inventories)
# =============================================================================
@router.get("/stocks/inventories", response_model=List[StockInventoryResponse], summary="Lister les inventaires physiques")
def list_inventories(
    location_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    inventories, _ = service.get_inventories(location_id=location_id, status_filter=status, skip=skip, limit=limit)
    return inventories


@router.post("/stocks/inventories", response_model=StockInventoryResponse, status_code=status.HTTP_201_CREATED, summary="Créer une session d'inventaire")
def create_inventory(
    data: StockInventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.create_inventory(data, user_id=current_user.id)


@router.get("/stocks/inventories/{inventory_id}", response_model=StockInventoryResponse, summary="Détail d'un inventaire avec écarts")
def get_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_inventory_by_id(inventory_id)


@router.post("/stocks/inventories/{inventory_id}/validate", response_model=StockInventoryResponse, summary="Valider un inventaire et ajuster le stock")
def validate_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.validate_inventory(inventory_id, user_id=current_user.id)


# =============================================================================
# 8. TABLEAUX DE BORD & ANALYTIQUES
# =============================================================================
@router.get("/purchases/dashboard/stats", response_model=PurchaseDashboardResponse, summary="Statistiques globales des achats")
def get_purchases_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_purchases_dashboard()


@router.get("/stocks/dashboard/stats", response_model=StockDashboardResponse, summary="Statistiques et alertes stock")
def get_stock_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_stock_dashboard()


@router.get("/chantiers/{chantier_id}/consumption", response_model=ChantierConsumptionResponse, summary="Consommation et achats pour un chantier donné")
def get_chantier_consumption(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    return service.get_chantier_consumption(chantier_id=chantier_id)
