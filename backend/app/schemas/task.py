from typing import Optional, List, Any
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# -----------------------------------------------------------------------------
# Responsable Short
# -----------------------------------------------------------------------------
class ResponsableShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    role_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


# -----------------------------------------------------------------------------
# Phase Schemas
# -----------------------------------------------------------------------------
class PhaseBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50, description="Code phase (ex: PHS-01)")
    name: str = Field(..., min_length=2, max_length=255, description="Nom de la phase / lot")
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    start_date_planned: Optional[date] = None
    end_date_planned: Optional[date] = None
    status: str = Field("À faire", description="Statut : À faire, En cours, En attente, Bloquée, Terminée, Annulée")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Pourcentage de progression")
    display_order: int = Field(1, description="Ordre d'affichage")


class PhaseCreate(PhaseBase):
    chantier_id: int = Field(..., description="ID du chantier associé")


class PhaseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    start_date_planned: Optional[date] = None
    end_date_planned: Optional[date] = None
    status: Optional[str] = None
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    display_order: Optional[int] = None


class PhaseResponse(PhaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chantier_id: int
    code: str
    tasks_count: Optional[int] = 0
    responsible: Optional[ResponsableShort] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# -----------------------------------------------------------------------------
# Task Dependency Schemas
# -----------------------------------------------------------------------------
class TaskDependencyBase(BaseModel):
    predecessor_id: int = Field(..., description="ID de la tâche antécédente (doit finir avant)")
    dependency_type: str = Field("FINISH_TO_START", description="Type : FINISH_TO_START")
    lag_days: int = Field(0, description="Décalage en jours (positif ou négatif)")


class TaskDependencyCreate(TaskDependencyBase):
    pass


class TaskDependencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    predecessor_id: int
    successor_id: int
    dependency_type: str
    lag_days: int
    predecessor_code: Optional[str] = None
    predecessor_name: Optional[str] = None
    predecessor_status: Optional[str] = None
    predecessor_progress: Optional[float] = None


# -----------------------------------------------------------------------------
# Task Schemas
# -----------------------------------------------------------------------------
class TaskBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50, description="Code unique tâche (ex: TSK-001)")
    name: str = Field(..., min_length=2, max_length=255, description="Nom / Intitulé de la tâche")
    description: Optional[str] = None

    chantier_id: int = Field(..., description="ID du chantier associé")
    phase_id: int = Field(..., description="ID de la phase / lot")
    parent_task_id: Optional[int] = Field(None, description="ID de la tâche parente (si sous-tâche)")
    responsible_id: Optional[int] = Field(None, description="ID du responsable assigné")

    status: str = Field("À faire", description="Statut : À faire, En cours, En attente, Bloquée, Terminée, Annulée")
    priority: str = Field("Normale", description="Priorité : Faible, Normale, Importante, Critique")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Progression 0-100%")
    weight: float = Field(1.0, ge=0.0, description="Poids de la tâche dans la phase/chantier")

    planned_start_date: date = Field(..., description="Date de début prévisionnelle")
    planned_end_date: date = Field(..., description="Date de fin prévisionnelle")
    estimated_duration_days: Optional[int] = Field(1, description="Durée estimée en jours")

    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None

    is_blocked: bool = Field(False, description="La tâche est-elle bloquée ?")
    blocking_reason: Optional[str] = Field(None, max_length=255, description="Motif de blocage")
    blocking_date: Optional[date] = None
    blocking_comment: Optional[str] = None
    blocking_impact: Optional[str] = None

    team_name: Optional[str] = Field(None, max_length=100)
    workers_count: int = Field(0, ge=0)
    equipment: Optional[str] = None
    materials: Optional[str] = None
    budget_estimated: Optional[float] = Field(0.0, ge=0.0)
    actual_cost: Optional[float] = Field(0.0, ge=0.0)

    observations: Optional[str] = None


class TaskCreate(TaskBase):
    predecessor_ids: Optional[List[int]] = Field(default=[], description="Liste des IDs de tâches dépendantes antérieures")


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phase_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    responsible_id: Optional[int] = None

    status: Optional[str] = None
    priority: Optional[str] = None
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    weight: Optional[float] = Field(None, ge=0.0)

    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    estimated_duration_days: Optional[int] = None

    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None

    is_blocked: Optional[bool] = None
    blocking_reason: Optional[str] = None
    blocking_date: Optional[date] = None
    blocking_comment: Optional[str] = None
    blocking_impact: Optional[str] = None

    team_name: Optional[str] = None
    workers_count: Optional[int] = None
    equipment: Optional[str] = None
    materials: Optional[str] = None
    budget_estimated: Optional[float] = None
    actual_cost: Optional[float] = None

    observations: Optional[str] = None
    predecessor_ids: Optional[List[int]] = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    delay_days: int = 0
    phase_name: Optional[str] = None
    responsible_name: Optional[str] = None
    parent_task_name: Optional[str] = None
    responsible: Optional[ResponsableShort] = None
    dependencies: List[TaskDependencyResponse] = []
    subtasks_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskTreeResponse(TaskResponse):
    subtasks: List["TaskTreeResponse"] = []


# -----------------------------------------------------------------------------
# Milestone Schemas
# -----------------------------------------------------------------------------
class MilestoneBase(BaseModel):
    code: Optional[str] = Field(None, max_length=50, description="Code jalon (ex: JAL-01)")
    name: str = Field(..., min_length=2, max_length=255, description="Nom du jalon")
    description: Optional[str] = None
    chantier_id: int = Field(..., description="ID du chantier")
    responsible_id: Optional[int] = None
    planned_date: date = Field(..., description="Date cible prévue")
    actual_date: Optional[date] = None
    status: str = Field("À venir", description="Statut : À venir, Atteint, En retard")


class MilestoneCreate(MilestoneBase):
    pass


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    planned_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[str] = None


class MilestoneResponse(MilestoneBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    responsible: Optional[ResponsableShort] = None
    responsible_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# -----------------------------------------------------------------------------
# Task History & Planning Overview
# -----------------------------------------------------------------------------
class TaskHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    comment: Optional[str] = None
    created_at: datetime
    user_name: Optional[str] = None


class PlanningOverviewResponse(BaseModel):
    chantier_id: int
    chantier_code: str
    chantier_name: str
    physical_progress: float
    total_phases: int
    total_tasks: int
    completed_tasks: int
    delayed_tasks: int
    blocked_tasks: int
    phases: List[PhaseResponse]
    tasks_tree: List[TaskTreeResponse]
    milestones: List[MilestoneResponse]


class NextTaskCodeResponse(BaseModel):
    code: str
