from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.chantier import ChantierService
from app.schemas.chantier import (
    ChantierCreate,
    ChantierResponse,
    ChantierListResponse,
    ChantierTypeCreate,
    ChantierTypeResponse,
    ResponsableCreate,
    ResponsableResponse,
    ClientCreate,
    ClientResponse,
    ChantierDocumentResponse,
    NextCodeResponse,
)

router = APIRouter(
    prefix="",
    tags=["Gestion des Chantiers & Référentiels BTP"],
)


# -----------------------------------------------------------------------------
# 1. Code Chantier Séquentiel Automatique
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/code/next",
    response_model=NextCodeResponse,
    summary="Obtenir le prochain code chantier disponible (ex: CH-2026-001)",
)
def get_next_chantier_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    next_code, year, seq = service.generate_next_code()
    return {"next_code": next_code, "year": year, "sequence": seq}


# -----------------------------------------------------------------------------
# 2. Types de Chantier (Référentiel dynamique)
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/types",
    response_model=List[ChantierTypeResponse],
    summary="Lister tous les types de chantiers disponibles",
)
def list_chantier_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.list_types()


@router.post(
    "/chantiers/types",
    response_model=ChantierTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau type de chantier dynamique",
)
def create_chantier_type(
    type_in: ChantierTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.create_type(type_in)


# -----------------------------------------------------------------------------
# 3. Responsables & Intervenants BTP (Référentiel dynamique)
# -----------------------------------------------------------------------------
@router.get(
    "/responsables",
    response_model=List[ResponsableResponse],
    summary="Lister les responsables de chantier (optionnellement filtrés par rôle)",
)
def list_responsables(
    role: Optional[str] = Query(None, description="Filtrer par rôle, ex: Chef de projet"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.list_responsables(role_name=role)


@router.post(
    "/responsables",
    response_model=ResponsableResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau responsable de chantier",
)
def create_responsable(
    resp_in: ResponsableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.create_responsable(resp_in)


# -----------------------------------------------------------------------------
# 4. Clients
# -----------------------------------------------------------------------------
@router.get(
    "/clients",
    response_model=List[ClientResponse],
    summary="Lister les clients",
)
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.list_clients()


@router.post(
    "/clients",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un client",
)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.create_client(client_in)


# -----------------------------------------------------------------------------
# 5. Chantiers (Création & Consultation)
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers",
    response_model=List[ChantierListResponse],
    summary="Lister les chantiers existants",
)
def list_chantiers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filtrer par statut"),
    search: Optional[str] = Query(None, description="Recherche textuelle par code, nom ou ville"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.list_chantiers(skip=skip, limit=limit, status=status, search=search)


@router.post(
    "/chantiers",
    response_model=ChantierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau chantier (ou enregistrer comme brouillon)",
)
def create_chantier(
    chantier_in: ChantierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.create_chantier(chantier_in, current_user_id=current_user.id)


@router.get(
    "/chantiers/{chantier_id}",
    response_model=ChantierResponse,
    summary="Obtenir les détails complets d'un chantier",
)
def get_chantier(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    chantier = service.get_chantier_by_id(chantier_id)
    if not chantier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chantier #{chantier_id} introuvable.",
        )
    return chantier


@router.post(
    "/chantiers/{chantier_id}/documents",
    response_model=ChantierDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Téléverser un document pour un chantier",
)
def upload_chantier_document(
    chantier_id: int,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChantierService(db)
    return service.add_document(
        chantier_id=chantier_id,
        document_type=document_type,
        upload_file=file,
    )
