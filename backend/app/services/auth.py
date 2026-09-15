from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.token import Token


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ce compte utilisateur est désactivé. Veuillez contacter un administrateur.",
            )
        return user

    def create_user_token(self, user: User) -> Token:
        access_token = create_access_token(
            subject=user.id,
            role=user.role.value,
        )
        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user.role.value,
            user_id=user.id,
            email=user.email,
        )
