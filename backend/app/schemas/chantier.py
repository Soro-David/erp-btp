from typing import Optional, List, Any
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# -----------------------------------------------------------------------------
# 1. Schémas Type de Chantier
# -----------------------------------------------------------------------------
class ChantierTypeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nom du type de chantier")
    description: Optional[str] = Field(None, max_length=500, description="Description optionnelle")


class ChantierTypeCreate(ChantierTypeBase):
    pass


class ChantierTypeResponse(ChantierTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: Optional[datetime] = None


# -----------------------------------------------------------------------------
# 2. Schémas Client
# -----------------------------------------------------------------------------
class ClientBase(BaseModel):
    type: str = Field("Particulier", description="Type de client : Particulier, Entreprise, Administration publique")
    name: str = Field(..., min_length=2, max_length=255, description="Nom ou Raison sociale")
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None

    # Conditionnels Entreprise
    company_name: Optional[str] = None
    rccm: Optional[str] = None
    company_contact: Optional[str] = None

    # Conditionnels Administration
    ministry: Optional[str] = None
    direction: Optional[str] = None
    service: Optional[str] = None
    admin_in_charge: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None


# -----------------------------------------------------------------------------
# 3. Schémas Responsable / Intervenant
# -----------------------------------------------------------------------------
class ResponsableBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None


class ResponsableCreate(ResponsableBase):
    pass


class ResponsableResponse(ResponsableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    full_name: str
    created_at: Optional[datetime] = None


# -----------------------------------------------------------------------------
# 4. Schémas Documents
# -----------------------------------------------------------------------------
class ChantierDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chantier_id: int
    document_type: str
    filename: str
    file_size: int
    mime_type: Optional[str] = None
    created_at: Optional[datetime] = None


# -----------------------------------------------------------------------------
# 5. Schémas Chantier Principal
# -----------------------------------------------------------------------------
class ChantierBase(BaseModel):
    code: Optional[str] = Field(None, description="Code unique chantier, ex: CH-2026-001 (généré si vide)")
    name: str = Field(..., min_length=2, max_length=255, description="Nom complet du chantier")
    description: Optional[str] = None

    type_id: Optional[int] = None
    type_name: Optional[str] = None
    status: str = Field("En préparation", description="En préparation, En cours, Suspendu, Terminé")

    # Localisation
    country: str = Field("Côte d'Ivoire")
    city: str = Field(..., min_length=2, max_length=100)
    commune: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Client
    client_id: Optional[int] = None
    client_name: Optional[str] = None

    # Responsables
    project_manager_id: Optional[int] = None
    site_manager_id: Optional[int] = None
    foreman_id: Optional[int] = None
    hse_officer_id: Optional[int] = None
    design_office: Optional[str] = None
    contractor: Optional[str] = None

    # Planning
    start_date_planned: date
    end_date_planned: date
    estimated_duration_days: Optional[int] = 0
    start_date_actual: Optional[date] = None
    end_date_actual: Optional[date] = None

    # Finances
    budget_estimated: Optional[float] = 0.0
    cost_estimated: Optional[float] = 0.0
    contract_amount: Optional[float] = 0.0
    currency: str = Field("FCFA")
    funding_mode: Optional[str] = Field("Fonds propres")

    # Technique
    surface_m2: Optional[float] = None
    buildings_count: Optional[int] = None
    floors_count: Optional[int] = None
    soil_nature: Optional[str] = None
    construction_method: Optional[str] = None
    technical_description: Optional[str] = None

    # Suivi
    physical_progress: float = Field(0.0, ge=0, le=100)
    financial_progress: float = Field(0.0, ge=0, le=100)
    priority: str = Field("Normale")

    observations: Optional[str] = None
    is_draft: bool = False


class ChantierCreate(ChantierBase):
    new_client: Optional[ClientCreate] = None


class ChantierUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type_id: Optional[int] = None
    type_name: Optional[str] = None
    status: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    commune: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    project_manager_id: Optional[int] = None
    site_manager_id: Optional[int] = None
    foreman_id: Optional[int] = None
    hse_officer_id: Optional[int] = None
    design_office: Optional[str] = None
    contractor: Optional[str] = None
    start_date_planned: Optional[date] = None
    end_date_planned: Optional[date] = None
    estimated_duration_days: Optional[int] = None
    start_date_actual: Optional[date] = None
    end_date_actual: Optional[date] = None
    budget_estimated: Optional[float] = None
    cost_estimated: Optional[float] = None
    contract_amount: Optional[float] = None
    currency: Optional[str] = None
    funding_mode: Optional[str] = None
    surface_m2: Optional[float] = None
    buildings_count: Optional[int] = None
    floors_count: Optional[int] = None
    soil_nature: Optional[str] = None
    construction_method: Optional[str] = None
    technical_description: Optional[str] = None
    physical_progress: Optional[float] = None
    financial_progress: Optional[float] = None
    priority: Optional[str] = None
    observations: Optional[str] = None
    is_draft: Optional[bool] = None


class ChantierResponse(ChantierBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Objets imbriqués optionnels
    chantier_type: Optional[ChantierTypeResponse] = None
    client: Optional[ClientResponse] = None
    project_manager: Optional[ResponsableResponse] = None
    site_manager: Optional[ResponsableResponse] = None
    foreman: Optional[ResponsableResponse] = None
    hse_officer: Optional[ResponsableResponse] = None
    documents: List[ChantierDocumentResponse] = []


class ChantierListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    status: str
    type_name: Optional[str] = None
    city: str
    client_name: Optional[str] = None
    start_date_planned: date
    end_date_planned: date
    estimated_duration_days: int
    budget_estimated: Optional[float] = 0.0
    contract_amount: Optional[float] = 0.0
    currency: str = "FCFA"
    physical_progress: float = 0.0
    priority: str = "Normale"
    is_draft: bool = False
    created_at: Optional[datetime] = None


class NextCodeResponse(BaseModel):
    next_code: str
    year: int
    sequence: int
