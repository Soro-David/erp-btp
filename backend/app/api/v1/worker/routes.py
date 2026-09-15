from fastapi import APIRouter, Depends
from app.api.v1.deps import require_roles, get_current_user
from app.models.user import User, UserRole

router = APIRouter(
    prefix="/worker",
    tags=["Worker - Espace Terrain & Pointages"],
    dependencies=[Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.OWNER,
        UserRole.DIRECTOR,
        UserRole.MANAGER,
        UserRole.WORKER,
    ]))],
)


@router.get("/daily-tasks", summary="Tâches du jour et saisie terrain")
def get_worker_tasks(current_user: User = Depends(get_current_user)):
    return {
        "role": current_user.role.value,
        "user": f"{current_user.first_name} {current_user.last_name}",
        "message": "Bienvenue dans l'espace Terrain / Chef de Chantier",
        "modules": [
            "Pointage quotidien des présences ouvriers",
            "Saisie des quantités réalisées par tâche",
            "Consommation des matériaux et bons de sortie",
            "Rapport de journal de chantier",
        ],
    }
