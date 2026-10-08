import secrets
from typing import List, Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, OwnerInviteRequest, CompleteInvitationRequest, ProfileUpdate
from app.core.security import hash_password, create_invitation_token, decode_invitation_token
from app.services.email import send_invitation_email


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
            company_name=user_in.company_name.strip() if user_in.company_name else None,
            company_logo=user_in.company_logo,
        )
        return self.repo.create(db_user)

    def invite_owner(self, invite_data: OwnerInviteRequest) -> Tuple[User, str, str]:
        """
        Invite un profil Owner en créant son compte en attente (is_active=False),
        génère un code OTP à 4 chiffres et lui envoie un email d'invitation avec le lien.
        """
        email_clean = invite_data.email.lower().strip()
        existing_user = self.repo.get_by_email(email_clean)

        # Génération du code OTP de 4 chiffres aléatoires (1000 à 9999)
        otp_code = f"{secrets.randbelow(9000) + 1000}"

        if existing_user:
            if existing_user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Un compte actif avec l'adresse email '{email_clean}' existe déjà.",
                )
            else:
                user = existing_user
                if invite_data.first_name:
                    user.first_name = invite_data.first_name.strip()
                if invite_data.last_name:
                    user.last_name = invite_data.last_name.strip()
                if invite_data.company_name:
                    user.company_name = invite_data.company_name.strip()
                if invite_data.company_logo:
                    user.company_logo = invite_data.company_logo
                user.otp_code = otp_code
                self.repo.update(user, {})
        else:
            temp_pwd = secrets.token_urlsafe(32)
            hashed_pwd = hash_password(temp_pwd)

            first_name = invite_data.first_name.strip() if invite_data.first_name and invite_data.first_name.strip() else "Propriétaire"
            last_name = invite_data.last_name.strip() if invite_data.last_name and invite_data.last_name.strip() else "BTP"

            db_user = User(
                email=email_clean,
                hashed_password=hashed_pwd,
                first_name=first_name,
                last_name=last_name,
                phone=None,
                role=UserRole.OWNER,
                is_active=False,  # Inactif tant que l'Owner n'a pas validé son inscription
                otp_code=otp_code,
                company_name=invite_data.company_name.strip() if invite_data.company_name else None,
                company_logo=invite_data.company_logo,
            )
            user = self.repo.create(db_user)

        # Génération du jeton d'invitation JWT sécurisé
        token = create_invitation_token(user.email, user.id)
        invitation_link = f"{settings.FRONTEND_URL}/activer-compte?token={token}&otp={otp_code}"

        # Envoi de l'email avec le code OTP à 4 chiffres et le lien d'accès
        full_name = f"{user.first_name} {user.last_name}".strip()
        send_invitation_email(
            to_email=user.email,
            invitation_link=invitation_link,
            otp_code=otp_code,
            recipient_name=full_name if full_name != "Propriétaire BTP" else None,
        )

        return user, invitation_link, otp_code

    def resend_invitation(self, user_id: int) -> Tuple[User, str, str]:
        """Renvoyer un email d'invitation avec un nouveau code OTP à 4 chiffres."""
        user = self.get_by_id(user_id)
        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce compte est déjà activé. Vous ne pouvez pas lui renvoyer d'invitation.",
            )

        otp_code = f"{secrets.randbelow(9000) + 1000}"
        user.otp_code = otp_code
        self.repo.update(user, {})

        token = create_invitation_token(user.email, user.id)
        invitation_link = f"{settings.FRONTEND_URL}/activer-compte?token={token}&otp={otp_code}"

        full_name = f"{user.first_name} {user.last_name}".strip()
        send_invitation_email(
            to_email=user.email,
            invitation_link=invitation_link,
            otp_code=otp_code,
            recipient_name=full_name if full_name != "Propriétaire BTP" else None,
        )

        return user, invitation_link, otp_code

    def get_invitation_info(self, token: str) -> dict:
        """Valide le jeton d'invitation et renvoie les détails pré-remplis pour la page d'activation."""
        payload = decode_invitation_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le lien d'invitation est invalide ou a expiré. Veuillez contacter votre administrateur.",
            )

        try:
            user_id = int(payload.get("sub"))
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Jeton d'invitation malformé.",
            )

        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="L'utilisateur associé à cette invitation n'existe plus.",
            )

        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce compte a déjà été activé. Vous pouvez vous connecter directement.",
            )

        return {
            "email": user.email,
            "first_name": user.first_name if user.first_name != "Propriétaire" else "",
            "last_name": user.last_name if user.last_name != "BTP" else "",
            "company_name": user.company_name or "",
            "company_logo": user.company_logo or "",
        }

    def complete_invitation(self, data: CompleteInvitationRequest) -> User:
        """Finalise l'inscription de l'Owner avec vérification du code OTP à 4 caractères."""
        payload = decode_invitation_token(data.token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le jeton d'invitation est invalide ou a expiré.",
            )

        try:
            user_id = int(payload.get("sub"))
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Jeton d'invitation malformé.",
            )

        user = self.get_by_id(user_id)
        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce compte a déjà été activé.",
            )

        # Vérification du code OTP à 4 chiffres
        if not user.otp_code or user.otp_code.strip() != data.otp.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code OTP invalide. Veuillez vérifier le code à 4 chiffres reçu par email.",
            )

        # Mise à jour des informations définitives et activation du compte
        update_dict = {
            "hashed_password": hash_password(data.password),
            "first_name": data.first_name.strip(),
            "last_name": data.last_name.strip(),
            "phone": data.phone.strip() if data.phone else None,
            "is_active": True,
            "otp_code": None,  # Consommé
        }
        if data.company_name:
            update_dict["company_name"] = data.company_name.strip()
        if data.company_logo:
            update_dict["company_logo"] = data.company_logo

        return self.repo.update(user, update_dict)

    def update_profile(self, user_id: int, profile_data: ProfileUpdate) -> User:
        """Mise à jour du profil de l'utilisateur connecté (dont nom entreprise et logo)."""
        user = self.get_by_id(user_id)
        update_dict = profile_data.model_dump(exclude_unset=True)

        if "first_name" in update_dict and update_dict["first_name"]:
            update_dict["first_name"] = update_dict["first_name"].strip()
        if "last_name" in update_dict and update_dict["last_name"]:
            update_dict["last_name"] = update_dict["last_name"].strip()
        if "phone" in update_dict and update_dict["phone"]:
            update_dict["phone"] = update_dict["phone"].strip()
        if "company_name" in update_dict and update_dict["company_name"]:
            update_dict["company_name"] = update_dict["company_name"].strip()

        return self.repo.update(user, update_dict)

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

