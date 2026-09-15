from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.token import Token
from app.schemas.user import UserLogin, UserResponse
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


@router.get("/me", response_model=UserResponse, summary="Obtenir le profil de l'utilisateur connecté")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Renvoie les informations de profil de l'utilisateur actuellement authentifié par JWT.
    """
    return current_user
