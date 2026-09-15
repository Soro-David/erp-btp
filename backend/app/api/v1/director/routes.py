from fastapi import APIRouter, Depends
from app.api.v1.deps import require_roles, get_current_user
from app.models.user import User, UserRole

router = APIRouter(
    prefix="/director",
    tags=["Director - Espace Direction Technique / Générale"],
    dependencies=[Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.OWNER, UserRole.DIRECTOR]))],
)


@router.get("/projects-overview", summary="Vue synthétique pour la Direction")
def get_director_overview(current_user: User = Depends(get_current_user)):
    return {
        "role": current_user.role.value,
        "user": f"{current_user.first_name} {current_user.last_name}",
        "message": "Bienvenue dans l'espace Direction Technique",
        "modules": [
            "Validation des situations de travaux",
            "Suivi des appels d'offres",
            "Supervision des contrats",
            "Allocation des ressources engins & équipes",
        ],
    }
