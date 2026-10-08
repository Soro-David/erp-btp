from typing import Optional, List
from datetime import date, datetime
from sqlalchemy import (
    String,
    Boolean,
    Text,
    Float,
    Integer,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="En cours", nullable=False)
    budget: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relations
    chantiers: Mapped[List["Chantier"]] = relationship("Chantier", back_populates="project")

    def __repr__(self) -> str:
        return f"<Project id={self.id} code='{self.code}' name='{self.name}'>"


class Phase(Base, TimestampMixin):
    __tablename__ = "phases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Ex: "Terrassement", "Gros œuvre"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    chantier_id: Mapped[int] = mapped_column(ForeignKey("chantiers.id", ondelete="CASCADE"), index=True, nullable=False)
    responsible_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)

    start_date_planned: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date_planned: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="À faire", nullable=False) # À faire, En cours, En attente, Bloquée, Terminée, Annulée
    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # 0 - 100 %
    display_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relations
    chantier: Mapped["Chantier"] = relationship("Chantier", back_populates="phases")
    responsible: Mapped[Optional["Responsable"]] = relationship("Responsable")
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="phase",
        cascade="all, delete-orphan",
        order_by="Task.planned_start_date",
    )

    def __repr__(self) -> str:
        return f"<Phase id={self.id} code='{self.code}' name='{self.name}'>"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: TSK-2026-001
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    chantier_id: Mapped[int] = mapped_column(ForeignKey("chantiers.id", ondelete="CASCADE"), index=True, nullable=False)
    phase_id: Mapped[int] = mapped_column(ForeignKey("phases.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=True)
    responsible_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)

    # Suivi & Priorité (deux informations distinctes selon CDC)
    status: Mapped[str] = mapped_column(String(50), default="À faire", nullable=False) # À faire, En cours, En attente, Bloquée, Terminée, Annulée
    priority: Mapped[str] = mapped_column(String(50), default="Normale", nullable=False) # Faible, Normale, Importante, Critique
    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # 0 à 100 %
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False) # Poids dans la phase

    # Planification
    planned_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    estimated_duration_days: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Réalisation réelle
    actual_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    actual_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    delay_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Gestion des blocages
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    blocking_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    blocking_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    blocking_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    blocking_impact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Ressources associées
    team_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    workers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    equipment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    materials: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    budget_estimated: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)
    actual_cost: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0, nullable=True)

    observations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relations
    chantier: Mapped["Chantier"] = relationship("Chantier", back_populates="tasks")
    phase: Mapped[Phase] = relationship("Phase", back_populates="tasks")
    responsible: Mapped[Optional["Responsable"]] = relationship("Responsable")

    # Sous-tâches
    parent_task: Mapped[Optional["Task"]] = relationship("Task", remote_side=[id], back_populates="subtasks")
    subtasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="parent_task",
        cascade="all, delete-orphan",
        order_by="Task.planned_start_date",
    )

    # Dépendances (Fin -> Début)
    dependencies_as_successor: Mapped[List["TaskDependency"]] = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.successor_id",
        back_populates="successor",
        cascade="all, delete-orphan",
    )
    dependencies_as_predecessor: Mapped[List["TaskDependency"]] = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.predecessor_id",
        back_populates="predecessor",
        cascade="all, delete-orphan",
    )

    # Historique
    history: Mapped[List["TaskHistory"]] = relationship(
        "TaskHistory",
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="desc(TaskHistory.created_at)",
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} code='{self.code}' name='{self.name}'>"


class TaskDependency(Base, TimestampMixin):
    __tablename__ = "task_dependencies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    predecessor_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    successor_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    dependency_type: Mapped[str] = mapped_column(String(50), default="FINISH_TO_START", nullable=False) # FINISH_TO_START
    lag_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relations
    predecessor: Mapped[Task] = relationship("Task", foreign_keys=[predecessor_id], back_populates="dependencies_as_predecessor")
    successor: Mapped[Task] = relationship("Task", foreign_keys=[successor_id], back_populates="dependencies_as_successor")

    __table_args__ = (
        CheckConstraint("predecessor_id != successor_id", name="check_no_self_dependency"),
    )

    def __repr__(self) -> str:
        return f"<TaskDependency id={self.id} {self.predecessor_id} -> {self.successor_id}>"


class Milestone(Base, TimestampMixin):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # JAL-01
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    chantier_id: Mapped[int] = mapped_column(ForeignKey("chantiers.id", ondelete="CASCADE"), index=True, nullable=False)
    responsible_id: Mapped[Optional[int]] = mapped_column(ForeignKey("responsables.id", ondelete="SET NULL"), nullable=True)

    planned_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="À venir", nullable=False) # À venir, Atteint, En retard

    # Relations
    chantier: Mapped["Chantier"] = relationship("Chantier", back_populates="milestones")
    responsible: Mapped[Optional["Responsable"]] = relationship("Responsable")

    def __repr__(self) -> str:
        return f"<Milestone id={self.id} code='{self.code}' name='{self.name}'>"


class TaskHistory(Base):
    __tablename__ = "task_histories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    task: Mapped[Task] = relationship("Task", back_populates="history")
    user: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<TaskHistory id={self.id} task_id={self.task_id} field='{self.field_name}'>"
