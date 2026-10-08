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

import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("uvicorn.error")


def _get_cors_headers(request: Request) -> dict:
    origin = request.headers.get("origin")
    cors_origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS]
    if origin and (origin in cors_origins or "*" in cors_origins):
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    return {}


# 1. Error catching middleware (inside CORSMiddleware so responses receive CORS headers)
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"Erreur non gérée sur {request.method} {request.url.path}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Erreur serveur interne : {str(exc)}"},
            headers=_get_cors_headers(request),
        )


# 2. Configuration CORS (added after middleware so it wraps outermost)
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur non gérée sur {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Erreur serveur interne : {str(exc)}"},
        headers=_get_cors_headers(request),
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


import os
from fastapi.staticfiles import StaticFiles

os.makedirs("uploads/purchases", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

from app.api.v1.router import api_router

# Enregistrement des routes API v1 (Auth, SuperAdmin, Owner, Director, Manager, Worker, Chantiers, Tasks, Achats)
app.include_router(api_router, prefix=settings.API_V1_STR)
