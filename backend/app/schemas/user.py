from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=30)
    role: UserRole = UserRole.WORKER
    is_active: bool = True
    company_name: Optional[str] = Field(None, max_length=255)
    company_logo: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Mot de passe avec au moins 8 caractères")


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)
    company_name: Optional[str] = Field(None, max_length=255)
    company_logo: Optional[str] = None


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = None
    company_name: Optional[str] = Field(None, max_length=255)
    company_logo: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OwnerInviteRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=255)
    company_logo: Optional[str] = None


class OwnerInviteResponse(BaseModel):
    user: UserResponse
    invitation_link: str
    otp_code: Optional[str] = None
    message: str


class InvitationInfoResponse(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None


class CompleteInvitationRequest(BaseModel):
    token: str
    otp: str = Field(..., min_length=4, max_length=10, description="Code OTP de validation (4 caractères)")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=30)
    password: str = Field(..., min_length=8, description="Nouveau mot de passe")
    company_name: Optional[str] = Field(None, max_length=255)
    company_logo: Optional[str] = None
