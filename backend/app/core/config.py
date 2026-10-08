import os
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "BTP Manager"
    API_V1_STR: str = "/api/v1"

    # Base de données PostgreSQL
    POSTGRES_USER: str = "btp_user"
    POSTGRES_PASSWORD: str = "btp_password_dev_2026"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "btp_manager"

    # Sécurité
    SECRET_KEY: str = "btp_manager_secret_key_change_in_production_32chars_min!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 heures
    INVITATION_TOKEN_EXPIRE_HOURS: int = 72     # 3 jours

    # Frontend URL (pour les liens d'activation)
    FRONTEND_URL: str = "http://localhost:5173"
    APP_NAME: str = "BTP Manager"

    # Configuration Emails (Supporte les formats standard MAIL_* et SMTP_*)
    MAIL_MAILER: str = "smtp"
    MAIL_SCHEME: Optional[str] = None
    MAIL_HOST: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM_ADDRESS: Optional[str] = None
    MAIL_FROM_NAME: Optional[str] = None

    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @property
    def EFFECTIVE_SMTP_HOST(self) -> Optional[str]:
        return self.MAIL_HOST or self.SMTP_HOST

    @property
    def EFFECTIVE_SMTP_PORT(self) -> int:
        return self.MAIL_PORT or self.SMTP_PORT or 587

    @property
    def EFFECTIVE_SMTP_USER(self) -> Optional[str]:
        return self.MAIL_USERNAME or self.SMTP_USER

    @property
    def EFFECTIVE_SMTP_PASSWORD(self) -> Optional[str]:
        return self.MAIL_PASSWORD or self.SMTP_PASSWORD

    @property
    def EFFECTIVE_FROM_EMAIL(self) -> str:
        return self.MAIL_FROM_ADDRESS or self.EMAILS_FROM_EMAIL or "sorodavi3@zohomail.com"

    @property
    def EFFECTIVE_FROM_NAME(self) -> str:
        return self.MAIL_FROM_NAME or self.EMAILS_FROM_NAME or self.APP_NAME


    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return []

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
