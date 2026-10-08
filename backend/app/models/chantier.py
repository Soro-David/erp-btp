from typing import Optional, List
from datetime import date
from sqlalchemy import (
    String,
    Boolean,
    Text,
    Float,
    Integer,
    Numeric,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class ChantierType(Base, TimestampMixin):
    __tablename__ = "chantier_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<ChantierType id={self.id} name='{self.name}'>"


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), default="Particulier", nullable=False) # Particulier, Entreprise, Administration publique
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Nom / Raison sociale
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_person: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Champs conditionnels Entreprise
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rccm: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Champs conditionnels Administration
    ministry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    direction: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    service: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    admin_in_charge: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Client id={self.id} name='{self.name}' type='{self.type}'>"


class Responsable(Base, TimestampMixin):
    __tablename__ = "responsables"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False) # Chef de projet, Conducteur des travaux, etc.
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<Responsable id={self.id} name='{self.full_name}' role='{self.role_name}'>"


class Chantier(Base, TimestampMixin):
    __tablename__ = "chantiers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Type de chantier
    type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chantier_types.id", ondelete="SET NULL"), nullable=True)
    type_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="En préparation", nullable=False) # En préparation, En cours, Suspendu, Terminé

    # Localisation
    country: Mapped[str] = mapped_column(String(100), default="Côte d'Ivoire", nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    commune: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Client
    client_id: Mapped[Optional[int]] = mapped_column(ForeignKey("clients.id", ondelete="SET NULL"), nullable=True)
    client_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Responsables assignés
    project_manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)
    site_manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)
    foreman_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)
    hse_officer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)
    design_office: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contractor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Planning
    start_date_planned: Mapped[date] = mapped_column(Date, nullable=False)
    end_date_planned: Mapped[date] = mapped_column(Date, nullable=False)
    estimated_duration_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    start_date_actual: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date_actual: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Informations financières
    budget_estimated: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    cost_estimated: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    contract_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="FCFA", nullable=False) # FCFA, EUR, USD
    funding_mode: Mapped[Optional[str]] = mapped_column(String(100), default="Fonds propres", nullable=True) # Fonds propres, Crédit, État, Bailleur, Autre

    # Informations techniques
    surface_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    buildings_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    floors_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    soil_nature: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    construction_method: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    technical_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Suivi initial
    physical_progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    financial_progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="Normale", nullable=False) # Faible, Normale, Élevée, Critique

    # Observations & statut brouillon
    observations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_draft: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)

    # Relations
    chantier_type: Mapped[Optional[ChantierType]] = relationship("ChantierType")
    client: Mapped[Optional[Client]] = relationship("Client")
    project_manager: Mapped[Optional[Responsable]] = relationship("Responsable", foreign_keys=[project_manager_id])
    site_manager: Mapped[Optional[Responsable]] = relationship("Responsable", foreign_keys=[site_manager_id])
    foreman: Mapped[Optional[Responsable]] = relationship("Responsable", foreign_keys=[foreman_id])
    hse_officer: Mapped[Optional[Responsable]] = relationship("Responsable", foreign_keys=[hse_officer_id])
    documents: Mapped[List["ChantierDocument"]] = relationship("ChantierDocument", back_populates="chantier", cascade="all, delete-orphan")

    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="chantiers")
    phases: Mapped[List["Phase"]] = relationship("Phase", back_populates="chantier", cascade="all, delete-orphan", order_by="Phase.display_order")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="chantier", cascade="all, delete-orphan")
    milestones: Mapped[List["Milestone"]] = relationship("Milestone", back_populates="chantier", cascade="all, delete-orphan", order_by="Milestone.planned_date")

    def __repr__(self) -> str:
        return f"<Chantier id={self.id} code='{self.code}' name='{self.name}'>"


class ChantierDocument(Base, TimestampMixin):
    __tablename__ = "chantier_documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chantier_id: Mapped[int] = mapped_column(ForeignKey("chantiers.id", ondelete="CASCADE"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False) # Contrat, Plan architectural, etc.
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    chantier: Mapped[Chantier] = relationship("Chantier", back_populates="documents")

    def __repr__(self) -> str:
        return f"<ChantierDocument id={self.id} filename='{self.filename}'>"
