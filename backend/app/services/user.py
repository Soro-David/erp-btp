from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé",
            )
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.repo.get_by_email(email)

    def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
    ) -> List[User]:
        return self.repo.get_all(skip=skip, limit=limit, role=role, is_active=is_active)

    def create_user(self, user_in: UserCreate) -> User:
        # Vérification unicité email
        existing_user = self.repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Un utilisateur avec l'email '{user_in.email}' existe déjà",
            )

        hashed_pwd = hash_password(user_in.password)
        db_user = User(
            email=user_in.email.lower().strip(),
            hashed_password=hashed_pwd,
            first_name=user_in.first_name.strip(),
            last_name=user_in.last_name.strip(),
            phone=user_in.phone.strip() if user_in.phone else None,
            role=user_in.role,
            is_active=user_in.is_active,
        )
        return self.repo.create(db_user)

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        update_data = user_update.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"]:
            new_email = update_data["email"].lower().strip()
            if new_email != user.email:
                existing = self.repo.get_by_email(new_email)
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"L'adresse email '{new_email}' est déjà utilisée",
                    )
                update_data["email"] = new_email

        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        return self.repo.update(user, update_data)

    def delete_user(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.repo.delete(user)
