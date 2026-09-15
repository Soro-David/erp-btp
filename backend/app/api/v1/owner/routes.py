from fastapi import APIRouter, Depends
from app.api.v1.deps import require_roles, get_current_user
from app.models.user import User, UserRole

router = APIRouter(
    prefix="/owner",
    tags=["Owner - Espace Propriétaire"],
    dependencies=[Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.OWNER]))],
)


@router.get("/dashboard-summary", summary="Vue synthétique pour le Propriétaire")
def get_owner_dashboard(current_user: User = Depends(get_current_user)):
    return {
        "role": current_user.role.value,
        "user": f"{current_user.first_name} {current_user.last_name}",
        "message": "Bienvenue dans l'espace Stratégie & Portefeuille Propriétaire",
        "modules": [
            "Vue globale rentabilité",
            "Portefeuille chantiers",
            "Approbation budgets",
            "Alertes trésorerie",
        ],
    }
