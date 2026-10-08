import re
from datetime import datetime, date
from typing import List, Optional, Tuple, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from sqlalchemy.exc import IntegrityError

from app.models.chantier import Chantier, Responsable
from app.models.task import Phase, Task, TaskDependency, Milestone, TaskHistory
from app.schemas.task import (
    PhaseCreate,
    PhaseUpdate,
    TaskCreate,
    TaskUpdate,
    TaskDependencyCreate,
    MilestoneCreate,
    MilestoneUpdate,
)


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------------------------
    # 1. Code Generators
    # -------------------------------------------------------------------------
    def generate_next_task_code(self, chantier_id: Optional[int] = None) -> str:
        """
        Génère un code de tâche unique du type TSK-YYYY-XXX.
        Garantit l'unicité globale requise par la contrainte unique sur tasks.code.
        """
        year = datetime.now().year
        prefix = f"TSK-{year}-"
        pattern = re.compile(rf"^TSK-{year}-(\d+)$")

        # Recherche globale de tous les codes de l'année pour respecter la contrainte UNIQUE
        existing = self.db.query(Task.code).filter(Task.code.like(f"{prefix}%")).all()
        max_seq = 0
        for (code,) in existing:
            if code:
                m = pattern.match(code.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        continue

        next_seq = max_seq + 1
        candidate_code = f"{prefix}{next_seq:03d}"

        # Double sécurité : vérifier directement qu'aucun enregistrement n'a ce code
        while self.db.query(Task.id).filter(Task.code == candidate_code).first() is not None:
            next_seq += 1
            candidate_code = f"{prefix}{next_seq:03d}"

        return candidate_code

    def generate_next_phase_code(self, chantier_id: int) -> str:
        """
        Génère un code de phase au format PHS-01, PHS-02...
        """
        existing = (
            self.db.query(Phase.code)
            .filter(Phase.chantier_id == chantier_id)
            .all()
        )
        pattern = re.compile(r"^PHS-(\d+)$")
        max_seq = 0
        for (code,) in existing:
            if code:
                m = pattern.match(code.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        continue
        return f"PHS-{max_seq + 1:02d}"

    def generate_next_milestone_code(self, chantier_id: int) -> str:
        """
        Génère un code de jalon au format JAL-01, JAL-02...
        """
        existing = (
            self.db.query(Milestone.code)
            .filter(Milestone.chantier_id == chantier_id)
            .all()
        )
        pattern = re.compile(r"^JAL-(\d+)$")
        max_seq = 0
        for (code,) in existing:
            if code:
                m = pattern.match(code.strip())
                if m:
                    try:
                        seq = int(m.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        continue
        return f"JAL-{max_seq + 1:02d}"

    # -------------------------------------------------------------------------
    # 2. Phase CRUD
    # -------------------------------------------------------------------------
    def list_phases(self, chantier_id: int) -> List[Phase]:
        phases = (
            self.db.query(Phase)
            .filter(Phase.chantier_id == chantier_id)
            .order_by(Phase.display_order.asc(), Phase.id.asc())
            .all()
        )
        # Populate tasks_count
        for p in phases:
            p.tasks_count = self.db.query(func.count(Task.id)).filter(Task.phase_id == p.id).scalar() or 0
        return phases

    def get_phase(self, phase_id: int) -> Phase:
        phase = self.db.query(Phase).filter(Phase.id == phase_id).first()
        if not phase:
            raise HTTPException(status_code=404, detail="Phase non trouvée")
        phase.tasks_count = self.db.query(func.count(Task.id)).filter(Task.phase_id == phase.id).scalar() or 0
        return phase

    def create_phase(self, phase_in: PhaseCreate) -> Phase:
        chantier = self.db.query(Chantier).filter(Chantier.id == phase_in.chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=404, detail="Chantier non trouvé")

        code = phase_in.code.strip() if phase_in.code else self.generate_next_phase_code(phase_in.chantier_id)

        phase = Phase(
            code=code,
            name=phase_in.name.strip(),
            description=phase_in.description.strip() if phase_in.description else None,
            chantier_id=phase_in.chantier_id,
            responsible_id=phase_in.responsible_id,
            start_date_planned=phase_in.start_date_planned,
            end_date_planned=phase_in.end_date_planned,
            status=phase_in.status or "À faire",
            progress=phase_in.progress or 0.0,
            display_order=phase_in.display_order or 1,
        )
        self.db.add(phase)
        self.db.commit()
        self.db.refresh(phase)
        phase.tasks_count = 0
        return phase

    def update_phase(self, phase_id: int, phase_in: PhaseUpdate) -> Phase:
        phase = self.get_phase(phase_id)
        update_data = phase_in.model_dump(exclude_unset=True)

        for key, val in update_data.items():
            if val is not None and isinstance(val, str):
                setattr(phase, key, val.strip())
            else:
                setattr(phase, key, val)

        self.db.commit()
        self.db.refresh(phase)
        self.recalculate_chantier_progress(phase.chantier_id)
        phase.tasks_count = self.db.query(func.count(Task.id)).filter(Task.phase_id == phase.id).scalar() or 0
        return phase

    def delete_phase(self, phase_id: int) -> bool:
        phase = self.get_phase(phase_id)
        chantier_id = phase.chantier_id
        self.db.delete(phase)
        self.db.commit()
        self.recalculate_chantier_progress(chantier_id)
        return True

    # -------------------------------------------------------------------------
    # 3. Task Helpers & Validation
    # -------------------------------------------------------------------------
    def _compute_task_delay(self, task: Task) -> int:
        """
        Calcule le nombre de jours de retard.
        """
        today = date.today()
        if task.status == "Terminée":
            if task.actual_end_date and task.planned_end_date:
                diff = (task.actual_end_date - task.planned_end_date).days
                return max(0, diff)
            return 0
        else:
            if task.planned_end_date and today > task.planned_end_date:
                return (today - task.planned_end_date).days
            return 0

    def _format_task_dict(self, task: Task) -> Dict[str, Any]:
        """
        Formate une tâche avec champs calculés et relations pour TaskResponse.
        """
        delay = self._compute_task_delay(task)
        responsible_name = f"{task.responsible.first_name} {task.responsible.last_name}" if task.responsible else None
        phase_name = task.phase.name if task.phase else None
        parent_task_name = task.parent_task.name if task.parent_task else None

        deps_data = []
        for dep in task.dependencies_as_successor:
            pred = dep.predecessor
            if pred:
                deps_data.append({
                    "id": dep.id,
                    "predecessor_id": dep.predecessor_id,
                    "successor_id": dep.successor_id,
                    "dependency_type": dep.dependency_type,
                    "lag_days": dep.lag_days,
                    "predecessor_code": pred.code,
                    "predecessor_name": pred.name,
                    "predecessor_status": pred.status,
                    "predecessor_progress": pred.progress,
                })

        return {
            "id": task.id,
            "code": task.code,
            "name": task.name,
            "description": task.description,
            "chantier_id": task.chantier_id,
            "phase_id": task.phase_id,
            "parent_task_id": task.parent_task_id,
            "responsible_id": task.responsible_id,
            "status": task.status,
            "priority": task.priority,
            "progress": task.progress,
            "weight": task.weight,
            "planned_start_date": task.planned_start_date,
            "planned_end_date": task.planned_end_date,
            "estimated_duration_days": task.estimated_duration_days,
            "actual_start_date": task.actual_start_date,
            "actual_end_date": task.actual_end_date,
            "delay_days": delay,
            "is_blocked": task.is_blocked,
            "blocking_reason": task.blocking_reason,
            "blocking_date": task.blocking_date,
            "blocking_comment": task.blocking_comment,
            "blocking_impact": task.blocking_impact,
            "team_name": task.team_name,
            "workers_count": task.workers_count,
            "equipment": task.equipment,
            "materials": task.materials,
            "budget_estimated": float(task.budget_estimated) if task.budget_estimated is not None else 0.0,
            "actual_cost": float(task.actual_cost) if task.actual_cost is not None else 0.0,
            "observations": task.observations,
            "phase_name": phase_name,
            "responsible_name": responsible_name,
            "parent_task_name": parent_task_name,
            "responsible": task.responsible,
            "dependencies": deps_data,
            "subtasks_count": len(task.subtasks) if task.subtasks else 0,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }

    def _check_subtask_cycle(self, task_id: int, potential_parent_id: int) -> bool:
        """
        Vérifie qu'assigner potential_parent_id comme parent de task_id ne crée pas de cycle.
        """
        curr = potential_parent_id
        visited = {task_id}
        while curr is not None:
            if curr in visited:
                return True
            visited.add(curr)
            parent = self.db.query(Task.parent_task_id).filter(Task.id == curr).first()
            curr = parent[0] if parent else None
        return False

    def _check_dependency_cycle(self, predecessor_id: int, successor_id: int) -> bool:
        """
        Vérifie si ajouter predecessor -> successor crée un cycle de dépendances.
        Cycle s'il existe déjà un chemin menant de successor vers predecessor.
        """
        if predecessor_id == successor_id:
            return True

        visited = set()
        queue = [successor_id]
        while queue:
            curr = queue.pop(0)
            if curr == predecessor_id:
                return True
            visited.add(curr)
            # successeurs de curr
            next_tasks = (
                self.db.query(TaskDependency.successor_id)
                .filter(TaskDependency.predecessor_id == curr)
                .all()
            )
            for (nxt_id,) in next_tasks:
                if nxt_id not in visited:
                    queue.append(nxt_id)
        return False

    # -------------------------------------------------------------------------
    # 4. Task CRUD
    # -------------------------------------------------------------------------
    def list_tasks(
        self,
        chantier_id: int,
        phase_id: Optional[int] = None,
        status_filter: Optional[str] = None,
        priority_filter: Optional[str] = None,
        only_root: bool = False,
    ) -> List[Dict[str, Any]]:
        query = self.db.query(Task).filter(Task.chantier_id == chantier_id)

        if phase_id:
            query = query.filter(Task.phase_id == phase_id)
        if status_filter:
            query = query.filter(Task.status == status_filter)
        if priority_filter:
            query = query.filter(Task.priority == priority_filter)
        if only_root:
            query = query.filter(Task.parent_task_id.is_(None))

        tasks = query.order_by(Task.planned_start_date.asc(), Task.id.asc()).all()
        return [self._format_task_dict(t) for t in tasks]

    def get_task(self, task_id: int) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Tâche non trouvée")
        return task

    def get_task_formatted(self, task_id: int) -> Dict[str, Any]:
        task = self.get_task(task_id)
        return self._format_task_dict(task)

    def get_task_tree(self, chantier_id: int, phase_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retourne l'arborescence complète des tâches (Tâches mères avec sous-tâches imbriquées).
        """
        query = (
            self.db.query(Task)
            .filter(Task.chantier_id == chantier_id)
            .filter(Task.parent_task_id.is_(None))
        )
        if phase_id:
            query = query.filter(Task.phase_id == phase_id)

        root_tasks = query.order_by(Task.planned_start_date.asc(), Task.id.asc()).all()

        def build_tree(task: Task) -> Dict[str, Any]:
            data = self._format_task_dict(task)
            subtasks_data = []
            if task.subtasks:
                for sub in sorted(task.subtasks, key=lambda s: (s.planned_start_date, s.id)):
                    subtasks_data.append(build_tree(sub))
            data["subtasks"] = subtasks_data
            return data

        return [build_tree(t) for t in root_tasks]

    def create_task(self, task_in: TaskCreate, current_user_id: Optional[int] = None) -> Dict[str, Any]:
        # Validate chantier and phase
        chantier = self.db.query(Chantier).filter(Chantier.id == task_in.chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=404, detail="Chantier non trouvé")

        phase = self.db.query(Phase).filter(Phase.id == task_in.phase_id).first()
        if not phase:
            raise HTTPException(status_code=404, detail="Phase non trouvée")

        if phase.chantier_id != task_in.chantier_id:
            raise HTTPException(status_code=400, detail="La phase sélectionnée n'appartient pas à ce chantier")

        # Parent task validation
        if task_in.parent_task_id:
            parent = self.get_task(task_in.parent_task_id)
            if parent.chantier_id != task_in.chantier_id:
                raise HTTPException(status_code=400, detail="La tâche parente n'appartient pas au même chantier")

        # Code generation & Uniqueness guarantee
        if task_in.code and task_in.code.strip():
            candidate_code = task_in.code.strip()
            existing_code = self.db.query(Task.id).filter(Task.code == candidate_code).first()
            if existing_code:
                code = self.generate_next_task_code()
            else:
                code = candidate_code
        else:
            code = self.generate_next_task_code()

        # Dates validation & estimated duration
        planned_start = task_in.planned_start_date
        planned_end = task_in.planned_end_date
        if planned_end < planned_start:
            raise HTTPException(status_code=400, detail="La date de fin prévisionnelle doit être postérieure à la date de début")

        duration = (planned_end - planned_start).days + 1
        if task_in.estimated_duration_days and task_in.estimated_duration_days > 0:
            duration = task_in.estimated_duration_days

        # Progress & Status cohesion
        progress = float(task_in.progress) if task_in.progress is not None else 0.0
        status_val = task_in.status or "À faire"
        actual_end = task_in.actual_end_date

        if progress >= 100.0:
            status_val = "Terminée"
            if not actual_end:
                actual_end = date.today()
        elif status_val == "Terminée":
            progress = 100.0
            if not actual_end:
                actual_end = date.today()

        new_task = Task(
            code=code,
            name=task_in.name.strip(),
            description=task_in.description.strip() if task_in.description else None,
            chantier_id=task_in.chantier_id,
            phase_id=task_in.phase_id,
            parent_task_id=task_in.parent_task_id,
            responsible_id=task_in.responsible_id,
            status=status_val,
            priority=task_in.priority or "Normale",
            progress=progress,
            weight=task_in.weight if task_in.weight is not None else 1.0,
            planned_start_date=planned_start,
            planned_end_date=planned_end,
            estimated_duration_days=duration,
            actual_start_date=task_in.actual_start_date,
            actual_end_date=actual_end,
            is_blocked=task_in.is_blocked,
            blocking_reason=task_in.blocking_reason.strip() if task_in.blocking_reason else None,
            blocking_date=task_in.blocking_date,
            blocking_comment=task_in.blocking_comment.strip() if task_in.blocking_comment else None,
            blocking_impact=task_in.blocking_impact.strip() if task_in.blocking_impact else None,
            team_name=task_in.team_name.strip() if task_in.team_name else None,
            workers_count=task_in.workers_count or 0,
            equipment=task_in.equipment.strip() if task_in.equipment else None,
            materials=task_in.materials.strip() if task_in.materials else None,
            budget_estimated=task_in.budget_estimated or 0.0,
            actual_cost=task_in.actual_cost or 0.0,
            observations=task_in.observations.strip() if task_in.observations else None,
        )
        self.db.add(new_task)
        try:
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            # Double sécurité : assigner un code frais garanti unique et réinsérer
            new_task.code = self.generate_next_task_code()
            self.db.add(new_task)
            self.db.flush()

        # Add dependencies if provided
        if task_in.predecessor_ids:
            for pred_id in set(task_in.predecessor_ids):
                if pred_id and pred_id != new_task.id:
                    dep = TaskDependency(
                        predecessor_id=pred_id,
                        successor_id=new_task.id,
                        dependency_type="FINISH_TO_START",
                        lag_days=0,
                    )
                    self.db.add(dep)

        # Log history
        history = TaskHistory(
            task_id=new_task.id,
            user_id=current_user_id,
            field_name="creation",
            new_value=f"Création de la tâche '{new_task.name}'",
            comment="Création initiale",
        )
        self.db.add(history)

        try:
            self.db.commit()
            self.db.refresh(new_task)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Conflit d'intégrité lors de l'enregistrement de la tâche")

        # Recalculate parent task and chantier progress
        if new_task.parent_task_id:
            self._recalculate_parent_task_progress(new_task.parent_task_id)
        self.recalculate_chantier_progress(new_task.chantier_id)

        return self._format_task_dict(new_task)

    def update_task(self, task_id: int, task_in: TaskUpdate, current_user_id: Optional[int] = None) -> Dict[str, Any]:
        task = self.get_task(task_id)
        update_data = task_in.model_dump(exclude_unset=True)

        # Check subtask cycle if parent_task_id is being changed
        if "parent_task_id" in update_data and update_data["parent_task_id"] is not None:
            new_parent_id = update_data["parent_task_id"]
            if self._check_subtask_cycle(task.id, new_parent_id):
                raise HTTPException(status_code=400, detail="Impossible d'assigner une tâche fille ou descendante comme tâche parente")

        # Track history for key fields
        tracked_fields = ["status", "priority", "progress", "planned_start_date", "planned_end_date", "is_blocked", "responsible_id"]
        for field in tracked_fields:
            if field in update_data:
                old_val = str(getattr(task, field))
                new_val = str(update_data[field])
                if old_val != new_val:
                    history = TaskHistory(
                        task_id=task.id,
                        user_id=current_user_id,
                        field_name=field,
                        old_value=old_val,
                        new_value=new_val,
                        comment=f"Modification de {field}",
                    )
                    self.db.add(history)

        # Cohesion between progress and status
        if "progress" in update_data and update_data["progress"] is not None:
            if update_data["progress"] >= 100.0:
                update_data["status"] = "Terminée"
                if not task.actual_end_date and not update_data.get("actual_end_date"):
                    update_data["actual_end_date"] = date.today()
        elif "status" in update_data and update_data["status"] == "Terminée":
            update_data["progress"] = 100.0
            if not task.actual_end_date and not update_data.get("actual_end_date"):
                update_data["actual_end_date"] = date.today()

        # Predecessors handling if specified
        if "predecessor_ids" in update_data and update_data["predecessor_ids"] is not None:
            new_pred_ids = set(update_data.pop("predecessor_ids"))
            # Check for cycles
            for pred_id in new_pred_ids:
                if pred_id == task.id:
                    raise HTTPException(status_code=400, detail="Une tâche ne peut pas dépendre d'elle-même")
                if self._check_dependency_cycle(pred_id, task.id):
                    raise HTTPException(status_code=400, detail=f"Dépendance circulaire détectée avec la tâche ID {pred_id}")

            # Delete existing dependencies as successor
            self.db.query(TaskDependency).filter(TaskDependency.successor_id == task.id).delete()
            for pred_id in new_pred_ids:
                self.db.add(TaskDependency(
                    predecessor_id=pred_id,
                    successor_id=task.id,
                    dependency_type="FINISH_TO_START",
                    lag_days=0,
                ))

        # Apply updates
        for key, val in update_data.items():
            if val is not None and isinstance(val, str):
                setattr(task, key, val.strip())
            else:
                setattr(task, key, val)

        # Recompute duration if dates changed
        if task.planned_end_date and task.planned_start_date:
            if task.planned_end_date < task.planned_start_date:
                raise HTTPException(status_code=400, detail="La date de fin prévisionnelle doit être postérieure à la date de début")
            task.estimated_duration_days = (task.planned_end_date - task.planned_start_date).days + 1

        task.delay_days = self._compute_task_delay(task)

        self.db.commit()
        self.db.refresh(task)

        # Recalculate parent task progress if applicable
        if task.parent_task_id:
            self._recalculate_parent_task_progress(task.parent_task_id)
        self.recalculate_chantier_progress(task.chantier_id)

        return self._format_task_dict(task)

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        chantier_id = task.chantier_id
        parent_id = task.parent_task_id

        self.db.delete(task)
        self.db.commit()

        if parent_id:
            self._recalculate_parent_task_progress(parent_id)
        self.recalculate_chantier_progress(chantier_id)
        return True

    def _recalculate_parent_task_progress(self, parent_task_id: int):
        """
        Recalcule la progression de la tâche mère en fonction de la moyenne pondérée de ses sous-tâches.
        """
        subtasks = self.db.query(Task).filter(Task.parent_task_id == parent_task_id).all()
        if not subtasks:
            return

        total_weight = sum(s.weight for s in subtasks if s.weight > 0) or len(subtasks)
        weighted_progress = sum(s.progress * (s.weight if s.weight > 0 else 1.0) for s in subtasks)
        avg_progress = round(weighted_progress / total_weight, 1)

        parent = self.db.query(Task).filter(Task.id == parent_task_id).first()
        if parent:
            parent.progress = min(100.0, max(0.0, avg_progress))
            if parent.progress >= 100.0:
                parent.status = "Terminée"
            elif parent.status == "Terminée" and parent.progress < 100.0:
                parent.status = "En cours"
            self.db.commit()
            if parent.parent_task_id:
                self._recalculate_parent_task_progress(parent.parent_task_id)

    # -------------------------------------------------------------------------
    # 5. Dependencies CRUD
    # -------------------------------------------------------------------------
    def add_dependency(self, successor_id: int, dep_in: TaskDependencyCreate) -> TaskDependency:
        pred_id = dep_in.predecessor_id
        if pred_id == successor_id:
            raise HTTPException(status_code=400, detail="Une tâche ne peut pas dépendre d'elle-même")

        pred_task = self.get_task(pred_id)
        succ_task = self.get_task(successor_id)

        if pred_task.chantier_id != succ_task.chantier_id:
            raise HTTPException(status_code=400, detail="Les tâches doivent appartenir au même chantier")

        # Check existing
        existing = (
            self.db.query(TaskDependency)
            .filter(TaskDependency.predecessor_id == pred_id)
            .filter(TaskDependency.successor_id == successor_id)
            .first()
        )
        if existing:
            return existing

        # Cycle detection
        if self._check_dependency_cycle(pred_id, successor_id):
            raise HTTPException(status_code=400, detail="Dépendance circulaire détectée : cette dépendance créerait une boucle infinie")

        dep = TaskDependency(
            predecessor_id=pred_id,
            successor_id=successor_id,
            dependency_type=dep_in.dependency_type or "FINISH_TO_START",
            lag_days=dep_in.lag_days or 0,
        )
        self.db.add(dep)
        self.db.commit()
        self.db.refresh(dep)
        return dep

    def remove_dependency(self, dependency_id: int) -> bool:
        dep = self.db.query(TaskDependency).filter(TaskDependency.id == dependency_id).first()
        if not dep:
            raise HTTPException(status_code=404, detail="Dépendance non trouvée")
        self.db.delete(dep)
        self.db.commit()
        return True

    # -------------------------------------------------------------------------
    # 6. Milestone CRUD
    # -------------------------------------------------------------------------
    def list_milestones(self, chantier_id: int) -> List[Milestone]:
        today = date.today()
        milestones = (
            self.db.query(Milestone)
            .filter(Milestone.chantier_id == chantier_id)
            .order_by(Milestone.planned_date.asc())
            .all()
        )
        # Update auto-status for past milestones not marked reached
        for m in milestones:
            if m.status != "Atteint" and m.planned_date < today:
                m.status = "En retard"
            m.responsible_name = f"{m.responsible.first_name} {m.responsible.last_name}" if m.responsible else None
        return milestones

    def get_milestone(self, milestone_id: int) -> Milestone:
        m = self.db.query(Milestone).filter(Milestone.id == milestone_id).first()
        if not m:
            raise HTTPException(status_code=404, detail="Jalon non trouvé")
        m.responsible_name = f"{m.responsible.first_name} {m.responsible.last_name}" if m.responsible else None
        return m

    def create_milestone(self, milestone_in: MilestoneCreate) -> Milestone:
        chantier = self.db.query(Chantier).filter(Chantier.id == milestone_in.chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=404, detail="Chantier non trouvé")

        code = milestone_in.code.strip() if milestone_in.code else self.generate_next_milestone_code(milestone_in.chantier_id)

        status_val = milestone_in.status or "À venir"
        if milestone_in.planned_date < date.today() and status_val != "Atteint":
            status_val = "En retard"

        milestone = Milestone(
            code=code,
            name=milestone_in.name.strip(),
            description=milestone_in.description.strip() if milestone_in.description else None,
            chantier_id=milestone_in.chantier_id,
            responsible_id=milestone_in.responsible_id,
            planned_date=milestone_in.planned_date,
            actual_date=milestone_in.actual_date,
            status=status_val,
        )
        self.db.add(milestone)
        self.db.commit()
        self.db.refresh(milestone)
        milestone.responsible_name = f"{milestone.responsible.first_name} {milestone.responsible.last_name}" if milestone.responsible else None
        return milestone

    def update_milestone(self, milestone_id: int, milestone_in: MilestoneUpdate) -> Milestone:
        milestone = self.get_milestone(milestone_id)
        update_data = milestone_in.model_dump(exclude_unset=True)

        for key, val in update_data.items():
            if val is not None and isinstance(val, str):
                setattr(milestone, key, val.strip())
            else:
                setattr(milestone, key, val)

        if milestone.status != "Atteint" and milestone.planned_date < date.today():
            milestone.status = "En retard"

        self.db.commit()
        self.db.refresh(milestone)
        milestone.responsible_name = f"{milestone.responsible.first_name} {milestone.responsible.last_name}" if milestone.responsible else None
        return milestone

    def delete_milestone(self, milestone_id: int) -> bool:
        milestone = self.get_milestone(milestone_id)
        self.db.delete(milestone)
        self.db.commit()
        return True

    # -------------------------------------------------------------------------
    # 7. Global Chantier & Phase Progress Recalculation
    # -------------------------------------------------------------------------
    def recalculate_chantier_progress(self, chantier_id: int) -> float:
        """
        Recalcule la progression globale du chantier et de chaque phase.
        Règle : moyenne pondérée des tâches de premier niveau (root tasks).
        Synchronise automatiquement `chantiers.physical_progress`.
        """
        chantier = self.db.query(Chantier).filter(Chantier.id == chantier_id).first()
        if not chantier:
            return 0.0

        phases = self.db.query(Phase).filter(Phase.chantier_id == chantier_id).all()
        for phase in phases:
            phase_tasks = (
                self.db.query(Task)
                .filter(Task.phase_id == phase.id)
                .filter(Task.parent_task_id.is_(None))
                .all()
            )
            if phase_tasks:
                total_w = sum(t.weight for t in phase_tasks if t.weight > 0) or len(phase_tasks)
                weighted_p = sum(t.progress * (t.weight if t.weight > 0 else 1.0) for t in phase_tasks)
                phase.progress = round(min(100.0, max(0.0, weighted_p / total_w)), 1)
                if phase.progress >= 100.0:
                    phase.status = "Terminée"
                elif phase.progress > 0 and phase.status == "À faire":
                    phase.status = "En cours"
            else:
                phase.progress = 0.0

        all_root_tasks = (
            self.db.query(Task)
            .filter(Task.chantier_id == chantier_id)
            .filter(Task.parent_task_id.is_(None))
            .all()
        )

        if all_root_tasks:
            total_w = sum(t.weight for t in all_root_tasks if t.weight > 0) or len(all_root_tasks)
            weighted_p = sum(t.progress * (t.weight if t.weight > 0 else 1.0) for t in all_root_tasks)
            global_progress = round(min(100.0, max(0.0, weighted_p / total_w)), 1)
        else:
            global_progress = 0.0

        chantier.physical_progress = global_progress
        self.db.commit()
        return global_progress

    # -------------------------------------------------------------------------
    # 8. Planning Overview
    # -------------------------------------------------------------------------
    def get_chantier_planning(self, chantier_id: int) -> Dict[str, Any]:
        chantier = self.db.query(Chantier).filter(Chantier.id == chantier_id).first()
        if not chantier:
            raise HTTPException(status_code=404, detail="Chantier non trouvé")

        # Synchronize progress
        self.recalculate_chantier_progress(chantier_id)

        phases = self.list_phases(chantier_id)
        tasks_tree = self.get_task_tree(chantier_id)
        milestones = self.list_milestones(chantier_id)

        all_tasks = self.db.query(Task).filter(Task.chantier_id == chantier_id).all()
        today = date.today()
        delayed_count = 0
        blocked_count = 0
        completed_count = 0

        for t in all_tasks:
            if t.status == "Terminée":
                completed_count += 1
            if t.is_blocked:
                blocked_count += 1
            if self._compute_task_delay(t) > 0:
                delayed_count += 1

        return {
            "chantier_id": chantier.id,
            "chantier_code": chantier.code,
            "chantier_name": chantier.name,
            "physical_progress": chantier.physical_progress or 0.0,
            "total_phases": len(phases),
            "total_tasks": len(all_tasks),
            "completed_tasks": completed_count,
            "delayed_tasks": delayed_count,
            "blocked_tasks": blocked_count,
            "phases": phases,
            "tasks_tree": tasks_tree,
            "milestones": milestones,
        }

    # -------------------------------------------------------------------------
    # 9. Task History
    # -------------------------------------------------------------------------
    def get_task_history(self, task_id: int) -> List[Dict[str, Any]]:
        self.get_task(task_id) # ensure exists
        history = (
            self.db.query(TaskHistory)
            .filter(TaskHistory.task_id == task_id)
            .order_by(desc(TaskHistory.created_at))
            .all()
        )
        result = []
        for h in history:
            user_name = f"{h.user.first_name} {h.user.last_name}" if h.user else "Système"
            result.append({
                "id": h.id,
                "task_id": h.task_id,
                "field_name": h.field_name,
                "old_value": h.old_value,
                "new_value": h.new_value,
                "comment": h.comment,
                "created_at": h.created_at,
                "user_name": user_name,
            })
        return result
