from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.deps import require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse, OwnerInviteRequest, OwnerInviteResponse
from app.services.user import UserService

router = APIRouter(
    prefix="/superadmin",
    tags=["SuperAdmin - Gestion Utilisateurs"],
    dependencies=[Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.OWNER]))],
)


@router.get("/users", response_model=List[UserResponse], summary="Lister tous les utilisateurs")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """Lister les utilisateurs avec pagination et filtrage par rôle/statut."""
    user_service = UserService(db)
    return user_service.list_users(skip=skip, limit=limit, role=role, is_active=is_active)


@router.post("/invite-owner", response_model=OwnerInviteResponse, status_code=status.HTTP_201_CREATED, summary="Inviter un nouveau profil Owner par email")
def invite_owner(
    invite_data: OwnerInviteRequest,
    db: Session = Depends(get_db),
):
    """
    Invite un profil Propriétaire (Owner) d'entreprise BTP.
    Crée le compte en attente (is_active=False) et lui envoie un email sécurisé
    pour lui permettre de renseigner son mot de passe et finaliser ses informations.
    """
    user_service = UserService(db)
    user, link, otp = user_service.invite_owner(invite_data)
    return {
        "user": user,
        "invitation_link": link,
        "otp_code": otp,
        "message": f"Invitation envoyée avec succès à {user.email}.",
    }


@router.post("/users/{user_id}/resend-invitation", response_model=OwnerInviteResponse, summary="Renvoyer l'email d'invitation")
def resend_invitation(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Renvoie l'email d'invitation avec un nouveau jeton sécurisé et code OTP."""
    user_service = UserService(db)
    user, link, otp = user_service.resend_invitation(user_id)
    return {
        "user": user,
        "invitation_link": link,
        "otp_code": otp,
        "message": f"Nouvelle invitation envoyée avec succès à {user.email}.",
    }


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Créer un nouvel utilisateur")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Créer un nouvel utilisateur (Owner, Director, Manager, Worker, ou Super Admin).
    Le mot de passe est haché avec bcrypt.
    """
    user_service = UserService(db)
    return user_service.create_user(user_in)


@router.get("/users/{user_id}", response_model=UserResponse, summary="Obtenir le détail d'un utilisateur")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Récupérer un utilisateur par son identifiant unique."""
    user_service = UserService(db)
    return user_service.get_by_id(user_id)


@router.put("/users/{user_id}", response_model=UserResponse, summary="Modifier un utilisateur")
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """Mettre à jour les informations, le rôle ou le statut d'activation d'un utilisateur."""
    user_service = UserService(db)
    return user_service.update_user(user_id, user_update)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un utilisateur")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Supprimer définitivement un utilisateur de la base."""
    user_service = UserService(db)
    user_service.delete_user(user_id)
