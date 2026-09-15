import time
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuration CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", tags=["Root"])
def read_root():
    return {
        "app": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }


@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    start_time = time.time()
    try:
        # Test réel de la connexion PostgreSQL
        result = db.execute(text("SELECT version();")).scalar()
        query_duration_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "api_version": "v1",
            "database": {
                "status": "connected",
                "engine": "PostgreSQL",
                "version": result,
                "latency_ms": query_duration_ms,
            },
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": settings.PROJECT_NAME,
            "api_version": "v1",
            "database": {
                "status": "error",
                "error": str(e),
            },
        }


from app.api.v1.router import api_router

# Enregistrement des routes API v1 (Auth, SuperAdmin, Owner, Director, Manager, Worker)
app.include_router(api_router, prefix=settings.API_V1_STR)
