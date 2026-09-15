from fastapi import APIRouter, Depends
from app.api.v1.deps import require_roles, get_current_user
from app.models.user import User, UserRole

router = APIRouter(
    prefix="/manager",
    tags=["Manager - Espace Conduite de Travaux"],
    dependencies=[Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.OWNER, UserRole.DIRECTOR, UserRole.MANAGER]))],
)


@router.get("/assigned-sites", summary="Chantiers et tâches sous la responsabilité du manager")
def get_manager_sites(current_user: User = Depends(get_current_user)):
    return {
        "role": current_user.role.value,
        "user": f"{current_user.first_name} {current_user.last_name}",
        "message": "Bienvenue dans l'espace Conduite de Travaux & Projets",
        "modules": [
            "Planification phases et tâches",
            "Suivi de l'avancement physique et financier",
            "Demandes d'achats et réceptions",
            "Génération des situations de travaux",
        ],
    }
