from fastapi import APIRouter
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.superadmin.routes import router as superadmin_router
from app.api.v1.owner.routes import router as owner_router
from app.api.v1.director.routes import router as director_router
from app.api.v1.manager.routes import router as manager_router
from app.api.v1.worker.routes import router as worker_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(superadmin_router)
api_router.include_router(owner_router)
api_router.include_router(director_router)
api_router.include_router(manager_router)
api_router.include_router(worker_router)
