from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.task import TaskService
from app.schemas.task import (
    PhaseCreate,
    PhaseUpdate,
    PhaseResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskTreeResponse,
    TaskDependencyCreate,
    TaskDependencyResponse,
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneResponse,
    TaskHistoryResponse,
    PlanningOverviewResponse,
    NextTaskCodeResponse,
)

router = APIRouter(
    prefix="",
    tags=["Planification & Gestion des Tâches"],
)


# -----------------------------------------------------------------------------
# 1. Génération de Codes
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/{chantier_id}/tasks/next-code",
    response_model=NextTaskCodeResponse,
    summary="Générer automatiquement le prochain code de tâche (ex: TSK-2026-001)",
)
def get_next_task_code(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    code = service.generate_next_task_code(chantier_id)
    return {"code": code}


@router.get(
    "/chantiers/{chantier_id}/phases/next-code",
    summary="Générer automatiquement le prochain code de phase (ex: PHS-01)",
)
def get_next_phase_code(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    code = service.generate_next_phase_code(chantier_id)
    return {"code": code}


@router.get(
    "/chantiers/{chantier_id}/milestones/next-code",
    summary="Générer automatiquement le prochain code de jalon (ex: JAL-01)",
)
def get_next_milestone_code(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    code = service.generate_next_milestone_code(chantier_id)
    return {"code": code}


# -----------------------------------------------------------------------------
# 2. Phases / Lots
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/{chantier_id}/phases",
    response_model=List[PhaseResponse],
    summary="Lister toutes les phases d'un chantier",
)
def list_phases(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.list_phases(chantier_id)


@router.post(
    "/chantiers/{chantier_id}/phases",
    response_model=PhaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une nouvelle phase pour un chantier",
)
def create_phase(
    chantier_id: int,
    phase_in: PhaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if phase_in.chantier_id != chantier_id:
        phase_in.chantier_id = chantier_id
    service = TaskService(db)
    return service.create_phase(phase_in)


@router.get(
    "/phases/{phase_id}",
    response_model=PhaseResponse,
    summary="Obtenir les détails d'une phase",
)
def get_phase(
    phase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.get_phase(phase_id)


@router.put(
    "/phases/{phase_id}",
    response_model=PhaseResponse,
    summary="Mettre à jour une phase",
)
def update_phase(
    phase_id: int,
    phase_in: PhaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.update_phase(phase_id, phase_in)


@router.delete(
    "/phases/{phase_id}",
    summary="Supprimer une phase",
)
def delete_phase(
    phase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    service.delete_phase(phase_id)
    return {"success": True, "message": "Phase supprimée avec succès"}


# -----------------------------------------------------------------------------
# 3. Tâches & Sous-tâches
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/{chantier_id}/tasks",
    response_model=List[TaskResponse],
    summary="Lister les tâches d'un chantier avec filtres optionnels",
)
def list_tasks(
    chantier_id: int,
    phase_id: Optional[int] = Query(None, description="Filtrer par phase"),
    status: Optional[str] = Query(None, description="Filtrer par statut"),
    priority: Optional[str] = Query(None, description="Filtrer par priorité"),
    only_root: bool = Query(False, description="Retourner uniquement les tâches mères"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.list_tasks(
        chantier_id=chantier_id,
        phase_id=phase_id,
        status_filter=status,
        priority_filter=priority,
        only_root=only_root,
    )


@router.get(
    "/chantiers/{chantier_id}/tasks/tree",
    response_model=List[TaskTreeResponse],
    summary="Obtenir l'arbre hiérarchique des tâches et sous-tâches d'un chantier",
)
def get_task_tree(
    chantier_id: int,
    phase_id: Optional[int] = Query(None, description="Filtrer par phase"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.get_task_tree(chantier_id, phase_id)


@router.post(
    "/chantiers/{chantier_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une tâche ou sous-tâche pour un chantier",
)
def create_task(
    chantier_id: int,
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if task_in.chantier_id != chantier_id:
        task_in.chantier_id = chantier_id
    service = TaskService(db)
    return service.create_task(task_in, current_user_id=current_user.id)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Obtenir les détails complets d'une tâche",
)
def get_task_details(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.get_task_formatted(task_id)


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Mettre à jour une tâche ou sous-tâche",
)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.update_task(task_id, task_in, current_user_id=current_user.id)


@router.delete(
    "/tasks/{task_id}",
    summary="Supprimer une tâche ou sous-tâche",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    service.delete_task(task_id)
    return {"success": True, "message": "Tâche supprimée avec succès"}


@router.get(
    "/tasks/{task_id}/history",
    response_model=List[TaskHistoryResponse],
    summary="Historique des modifications d'une tâche",
)
def get_task_history(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.get_task_history(task_id)


# -----------------------------------------------------------------------------
# 4. Dépendances entre Tâches
# -----------------------------------------------------------------------------
@router.post(
    "/tasks/{successor_id}/dependencies",
    summary="Ajouter une dépendance Fin -> Début à une tâche",
)
def add_dependency(
    successor_id: int,
    dep_in: TaskDependencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    dep = service.add_dependency(successor_id, dep_in)
    return {
        "id": dep.id,
        "predecessor_id": dep.predecessor_id,
        "successor_id": dep.successor_id,
        "dependency_type": dep.dependency_type,
        "lag_days": dep.lag_days,
        "message": "Dépendance ajoutée avec succès",
    }


@router.delete(
    "/task-dependencies/{dependency_id}",
    summary="Supprimer une dépendance entre deux tâches",
)
def remove_dependency(
    dependency_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    service.remove_dependency(dependency_id)
    return {"success": True, "message": "Dépendance supprimée avec succès"}


# -----------------------------------------------------------------------------
# 5. Jalons (Milestones)
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/{chantier_id}/milestones",
    response_model=List[MilestoneResponse],
    summary="Lister tous les jalons d'un chantier",
)
def list_milestones(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.list_milestones(chantier_id)


@router.post(
    "/chantiers/{chantier_id}/milestones",
    response_model=MilestoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau jalon",
)
def create_milestone(
    chantier_id: int,
    milestone_in: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if milestone_in.chantier_id != chantier_id:
        milestone_in.chantier_id = chantier_id
    service = TaskService(db)
    return service.create_milestone(milestone_in)


@router.put(
    "/milestones/{milestone_id}",
    response_model=MilestoneResponse,
    summary="Mettre à jour un jalon",
)
def update_milestone(
    milestone_id: int,
    milestone_in: MilestoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.update_milestone(milestone_id, milestone_in)


@router.delete(
    "/milestones/{milestone_id}",
    summary="Supprimer un jalon",
)
def delete_milestone(
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    service.delete_milestone(milestone_id)
    return {"success": True, "message": "Jalon supprimé avec succès"}


# -----------------------------------------------------------------------------
# 6. Planning Global du Chantier
# -----------------------------------------------------------------------------
@router.get(
    "/chantiers/{chantier_id}/planning",
    response_model=PlanningOverviewResponse,
    summary="Obtenir la vue d'ensemble du planning d'un chantier (Gantt, Tâches, Jalons, Phases)",
)
def get_chantier_planning(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return service.get_chantier_planning(chantier_id)


@router.post(
    "/chantiers/{chantier_id}/planning/recalculate",
    summary="Recalculer manuellement l'avancement global du chantier basé sur ses tâches",
)
def recalculate_planning(
    chantier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    progress = service.recalculate_chantier_progress(chantier_id)
    return {
        "chantier_id": chantier_id,
        "physical_progress": progress,
        "message": f"Progression physique recalculée : {progress}%",
    }
