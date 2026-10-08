from typing import Optional, List, Any, Dict
from datetime import date as dt_date, datetime as dt_datetime
from pydantic import BaseModel, Field, ConfigDict


# -----------------------------------------------------------------------------
# 1. Fournisseurs (Suppliers)
# -----------------------------------------------------------------------------
class SupplierBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50, description="Code unique fournisseur (ex: FOUR-001)")
    name: str = Field(..., min_length=2, max_length=255, description="Raison sociale ou Nom du fournisseur")
    trade_name: Optional[str] = Field(None, max_length=255, description="Nom commercial / Enseigne")
    contact_name: Optional[str] = Field(None, max_length=150, description="Nom et prénom du contact principal")
    phone: str = Field(..., min_length=5, max_length=50, description="Numéro de téléphone principal")
    email: Optional[str] = Field(None, max_length=255, description="Adresse email")
    address: Optional[str] = Field(None, max_length=255, description="Adresse physique")
    city: Optional[str] = Field("Abidjan", max_length=100)
    country: str = Field("Côte d'Ivoire", max_length=100)

    # Informations administratives
    rccm: Optional[str] = Field(None, max_length=100, description="RCCM")
    ncc: Optional[str] = Field(None, max_length=100, description="Numéro de Compte Contribuable")

    # Commercial
    payment_terms: Optional[str] = Field(None, max_length=255, description="Conditions de règlement habituelles")
    notes: Optional[str] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    trade_name: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    rccm: Optional[str] = None
    ncc: Optional[str] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierResponse(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchases_count: int = 0
    total_purchased_amount: float = 0.0
    created_at: Optional[dt_datetime] = None
    updated_at: Optional[dt_datetime] = None


class SupplierStatsResponse(BaseModel):
    supplier_id: int
    purchases_count: int
    total_purchased_amount: float
    total_paid_amount: float
    remaining_to_pay: float
    pending_orders_count: int
    last_purchase_date: Optional[dt_date] = None


# -----------------------------------------------------------------------------
# 2. Catégories & Unités de Matériaux
# -----------------------------------------------------------------------------
class MaterialCategoryBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class MaterialCategoryCreate(MaterialCategoryBase):
    pass


class MaterialCategoryUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class MaterialCategoryResponse(MaterialCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    materials_count: int = 0
    created_at: Optional[dt_datetime] = None


class MaterialUnitBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=20, description="Ex: SAC, T, BARRE, M3")
    name: str = Field(..., min_length=2, max_length=100, description="Ex: Sac, Tonne, Barre")


class MaterialUnitCreate(MaterialUnitBase):
    pass


class MaterialUnitUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None


class MaterialUnitResponse(MaterialUnitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 3. Matériaux (Materials)
# -----------------------------------------------------------------------------
class MaterialBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50, description="Code unique matériau (ex: MAT-2026-001)")
    name: str = Field(..., min_length=2, max_length=255, description="Désignation du matériau")
    description: Optional[str] = None
    category_id: int = Field(..., description="ID de la catégorie")
    unit_id: int = Field(..., description="ID de l'unité de mesure")
    reference: Optional[str] = Field(None, max_length=100, description="Référence fabricant ou commerciale")
    indicative_price: Optional[float] = Field(0.0, ge=0.0, description="Prix unitaire indicatif moyen")
    minimum_stock: float = Field(0.0, ge=0.0, description="Seuil d'alerte stock faible")
    maximum_stock: float = Field(0.0, ge=0.0, description="Capacité maximale conseillée")
    is_active: bool = True


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    reference: Optional[str] = None
    indicative_price: Optional[float] = None
    minimum_stock: Optional[float] = None
    maximum_stock: Optional[float] = None
    is_active: Optional[bool] = None


class MaterialResponse(MaterialBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: Optional[str] = None
    unit_name: Optional[str] = None
    unit_code: Optional[str] = None
    current_stock: float = 0.0
    stock_status: str = "Normal" # Normal, Stock faible, Rupture
    created_at: Optional[dt_datetime] = None
    updated_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 4. Emplacements de Stock (Stock Locations)
# -----------------------------------------------------------------------------
class StockLocationBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    location: Optional[str] = None
    type: str = Field("Dépôt principal", description="Dépôt principal, Magasin, Entrepôt")
    is_active: bool = True


class StockLocationCreate(StockLocationBase):
    pass


class StockLocationUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    is_active: Optional[bool] = None


class StockLocationResponse(StockLocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items_count: int = 0
    created_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 5. Lignes d'Achat & Réceptions (Purchase Lines & Receipts)
# -----------------------------------------------------------------------------
class PurchaseLineCreate(BaseModel):
    material_id: int
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    total_price: Optional[float] = None


class MaterialUnitMiniResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name: str


class MaterialMiniResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name: str
    indicative_price: Optional[float] = 0.0
    unit: Optional[MaterialUnitMiniResponse] = None


class PurchaseLineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchase_id: int
    material_id: int
    material_code: Optional[str] = None
    material_name: Optional[str] = None
    unit_code: Optional[str] = None
    material: Optional[MaterialMiniResponse] = None
    quantity: float
    unit_price: float
    total_price: float
    quantity_received: float = 0.0
    remaining_quantity: float = 0.0


class PurchaseReceiptItemCreate(BaseModel):
    purchase_line_id: int
    quantity_received: float = Field(..., gt=0)
    quantity_rejected: float = Field(0.0, ge=0)
    rejection_reason: Optional[str] = None


class PurchaseReceiptCreate(BaseModel):
    date: dt_date
    location_id: int = Field(..., description="Dépôt de réception des marchandises")
    notes: Optional[str] = None
    items: List[PurchaseReceiptItemCreate] = []


class PurchaseReceiptItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    receipt_id: int
    purchase_line_id: int
    material_id: int
    material_name: Optional[str] = None
    unit_code: Optional[str] = None
    quantity_received: float
    quantity_rejected: float
    rejection_reason: Optional[str] = None


class PurchaseReceiptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchase_id: int
    receipt_number: str
    date: dt_date
    location_id: int
    location_name: Optional[str] = None
    notes: Optional[str] = None
    items: List[PurchaseReceiptItemResponse] = []
    created_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 6. Documents d'Achat (Purchase Documents)
# -----------------------------------------------------------------------------
class PurchaseDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchase_id: int
    document_type: str
    document_number: Optional[str] = None
    document_date: Optional[dt_date] = None
    original_filename: str
    file_path: str
    file_url: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: int = 0
    uploaded_by: Optional[int] = None
    created_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 7. Achats (Purchases)
# -----------------------------------------------------------------------------
class PurchaseBase(BaseModel):
    reference: Optional[str] = Field(None, max_length=50, description="Référence achat (ex: ACH-2026-00001)")
    supplier_id: int = Field(..., description="ID du fournisseur sélectionné")
    chantier_id: int = Field(..., description="ID du chantier rattaché")
    task_id: Optional[int] = Field(None, description="ID de la tâche associée (optionnel)")
    date: dt_date = Field(..., description="Date d'émission de l'achat")
    status: str = Field("Brouillon", description="Brouillon, En attente, Validé, Commandé, Partiellement reçu, Reçu, Annulé, Clôturé")
    payment_status: str = Field("Non payé", description="Non payé, Partiellement payé, Payé")
    payment_mode: Optional[str] = Field("Virement", description="Espèces, Virement, Chèque, Mobile Money")
    subject: Optional[str] = Field(None, max_length=255, description="Objet synthétique de l'achat")
    notes: Optional[str] = None
    currency: Optional[str] = Field("FCFA", max_length=10, description="Devise (ex: FCFA, EUR)")
    is_quick_purchase: Optional[bool] = Field(False, description="Indique si c'est un achat rapide")


class PurchaseCreate(PurchaseBase):
    lines: List[PurchaseLineCreate] = Field(..., min_length=1, description="Articles commandés")


class QuickPurchaseItem(BaseModel):
    material_id: Optional[int] = None
    material_name: Optional[str] = None
    quantity: float = Field(1.0, gt=0)
    unit_price: float = Field(..., ge=0)


class QuickPurchaseCreate(BaseModel):
    """Formulaire simplifié d'achat direct sur le terrain (mobile-first)"""
    chantier_id: int
    task_id: Optional[int] = None
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = None # Si nouveau fournisseur ponctuel
    supplier_phone: Optional[str] = None
    material_id: Optional[int] = None
    material_name: Optional[str] = None # Si matériau non répertorié
    quantity: Optional[float] = Field(1.0, gt=0)
    unit_price: Optional[float] = Field(0.0, ge=0)
    items: Optional[List[QuickPurchaseItem]] = None
    auto_receive: bool = True
    location_id: Optional[int] = None
    date: Optional[dt_date] = None
    payment_status: Optional[str] = "Payé"
    payment_mode: str = "Espèces"
    subject: Optional[str] = None
    notes: Optional[str] = None


class PurchaseUpdate(BaseModel):
    supplier_id: Optional[int] = None
    chantier_id: Optional[int] = None
    task_id: Optional[int] = None
    date: Optional[dt_date] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    payment_mode: Optional[str] = None
    subject: Optional[str] = None
    notes: Optional[str] = None
    currency: Optional[str] = None
    is_quick_purchase: Optional[bool] = None
    lines: Optional[List[PurchaseLineCreate]] = None


class PurchaseChantierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: Optional[str] = None


class PurchaseTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: Optional[str] = None


class PurchaseResponse(PurchaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_amount: float
    currency: str = "FCFA"
    is_quick_purchase: bool = False
    supplier: Optional[SupplierResponse] = None
    chantier: Optional[PurchaseChantierResponse] = None
    task: Optional[PurchaseTaskResponse] = None
    supplier_name: Optional[str] = None
    chantier_code: Optional[str] = None
    chantier_name: Optional[str] = None
    task_code: Optional[str] = None
    task_name: Optional[str] = None
    reception_percentage: float = 0.0
    documents_count: int = 0
    created_at: Optional[dt_datetime] = None
    updated_at: Optional[dt_datetime] = None


class PurchaseDetailResponse(PurchaseResponse):
    lines: List[PurchaseLineResponse] = []
    receipts: List[PurchaseReceiptResponse] = []
    documents: List[PurchaseDocumentResponse] = []


# -----------------------------------------------------------------------------
# 8. Mouvements de Stock (Stock Movements)
# -----------------------------------------------------------------------------
class StockMovementBase(BaseModel):
    material_id: int
    location_id: int
    movement_type: str = Field(..., description="Entrée, Sortie, Transfert, Retour, Ajustement, Inventaire")
    quantity: float
    unit_price: Optional[float] = 0.0
    chantier_id: Optional[int] = None
    task_id: Optional[int] = None
    purchase_id: Optional[int] = None
    source_location_id: Optional[int] = None
    dest_location_id: Optional[int] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    pass


class StockIssueCreate(BaseModel):
    """Sortie de stock vers un chantier et tâche éventuelle"""
    location_id: int = Field(..., description="Dépôt source")
    chantier_id: int = Field(..., description="Chantier destinataire")
    task_id: Optional[int] = Field(None, description="Tâche spécifique consommatrice (optionnel)")
    material_id: int = Field(..., description="Matériau affecté")
    quantity: float = Field(..., gt=0, description="Quantité sortie")
    reason: Optional[str] = Field("Affectation chantier", max_length=255)
    notes: Optional[str] = None


class StockTransferCreate(BaseModel):
    """Transfert inter-dépôts"""
    source_location_id: int = Field(..., description="Dépôt d'origine")
    dest_location_id: int = Field(..., description="Dépôt de destination")
    material_id: int = Field(..., description="Matériau transféré")
    quantity: float = Field(..., gt=0, description="Quantité transférée")
    notes: Optional[str] = None


class StockReturnCreate(BaseModel):
    """Retour de chantier vers un dépôt"""
    chantier_id: int = Field(..., description="Chantier d'origine")
    task_id: Optional[int] = None
    location_id: int = Field(..., description="Dépôt de réintégration")
    material_id: int = Field(..., description="Matériau retourné")
    quantity: float = Field(..., gt=0, description="Quantité retournée")
    reason: Optional[str] = Field("Retour surplus de chantier", max_length=255)
    notes: Optional[str] = None


class StockMovementResponse(StockMovementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reference: str
    date: dt_datetime
    material_name: Optional[str] = None
    material_code: Optional[str] = None
    unit_code: Optional[str] = None
    location_name: Optional[str] = None
    source_location_name: Optional[str] = None
    dest_location_name: Optional[str] = None
    chantier_name: Optional[str] = None
    task_name: Optional[str] = None
    user_name: Optional[str] = None
    created_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 9. Inventaires (Inventories)
# -----------------------------------------------------------------------------
class StockInventoryItemCreate(BaseModel):
    material_id: int
    actual_quantity: float = Field(..., ge=0)
    notes: Optional[str] = None


class StockInventoryCreate(BaseModel):
    location_id: int
    inventory_date: dt_date
    notes: Optional[str] = None
    items: List[StockInventoryItemCreate] = []


class StockInventoryUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class StockInventoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inventory_id: int
    material_id: int
    material_name: Optional[str] = None
    material_code: Optional[str] = None
    unit_code: Optional[str] = None
    theoretical_quantity: float
    actual_quantity: float
    discrepancy: float
    unit_price: float = 0.0
    notes: Optional[str] = None


class StockInventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reference: str
    location_id: int
    location_name: Optional[str] = None
    inventory_date: dt_date
    status: str
    notes: Optional[str] = None
    created_by_name: Optional[str] = None
    items: List[StockInventoryItemResponse] = []
    created_at: Optional[dt_datetime] = None


# -----------------------------------------------------------------------------
# 10. Tableaux de Bord & Synthèses
# -----------------------------------------------------------------------------
class PurchaseDashboardResponse(BaseModel):
    total_purchases: int
    pending_purchases: int
    ordered_purchases: int
    partially_received_purchases: int
    received_purchases: int
    total_committed_amount: float
    total_paid_amount: float
    remaining_to_pay: float


class StockDashboardResponse(BaseModel):
    total_materials_count: int
    active_materials_count: int
    out_of_stock_count: int
    low_stock_count: int
    total_stock_value: float
    total_locations_count: int
    alerts: List[MaterialResponse] = []


class MaterialStockAtLocation(BaseModel):
    material_id: int
    material_code: str
    material_name: str
    category_name: str
    unit_code: str
    location_id: int
    location_name: str
    quantity: float
    indicative_price: float
    stock_value: float
    minimum_stock: float
    stock_status: str


class ChantierConsumptionResponse(BaseModel):
    chantier_id: int
    chantier_code: str
    chantier_name: str
    total_purchases_amount: float
    total_paid_amount: float
    remaining_to_pay: float
    materials_ordered: List[Dict[str, Any]] = []
    materials_issued: List[Dict[str, Any]] = []
