from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth import AuthService
from app.services.user import UserService
from app.schemas.token import Token
from app.schemas.user import (
    UserLogin,
    UserResponse,
    InvitationInfoResponse,
    CompleteInvitationRequest,
    ProfileUpdate,
)
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token, summary="Connexion utilisateur et émission du jeton JWT")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authentifie un utilisateur avec son email et son mot de passe,
    et renvoie un jeton d'accès JWT porteur de son rôle.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    return auth_service.create_user_token(user)


@router.get("/invitation-info", response_model=InvitationInfoResponse, summary="Vérifier la validité d'une invitation et récupérer les infos de base")
def get_invitation_info(
    token: str = Query(..., description="Jeton JWT d'invitation"),
    db: Session = Depends(get_db),
):
    """
    Permet à la page de finalisation du profil de valider le jeton
    et d'afficher l'adresse email de l'invité.
    """
    user_service = UserService(db)
    return user_service.get_invitation_info(token)


@router.post("/complete-invitation", response_model=Token, summary="Finaliser le profil Owner et activer le compte")
def complete_invitation(
    complete_data: CompleteInvitationRequest,
    db: Session = Depends(get_db),
):
    """
    Définit le mot de passe, les nom/prénom/téléphone de l'Owner,
    active son compte et le connecte immédiatement en émettant un jeton JWT.
    """
    user_service = UserService(db)
    user = user_service.complete_invitation(complete_data)
    auth_service = AuthService(db)
    return auth_service.create_user_token(user)


@router.get("/me", response_model=UserResponse, summary="Obtenir le profil de l'utilisateur connecté")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Renvoie les informations de profil de l'utilisateur actuellement authentifié par JWT.
    """
    return current_user


@router.put("/me", response_model=UserResponse, summary="Mettre à jour le profil de l'utilisateur connecté")
def update_me(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permet à l'utilisateur connecté (notamment Owner) de modifier ses informations
    personnelles, son nom d'entreprise et son logo.
    """
    user_service = UserService(db)
    return user_service.update_profile(current_user.id, profile_data)

