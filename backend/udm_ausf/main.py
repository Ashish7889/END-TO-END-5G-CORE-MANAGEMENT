from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.common.config import get_settings
from backend.common.db import init_db
from backend.udm_ausf.routers import auth as auth_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="UDM/AUSF Service",
        version="0.1.0",
        description="Subscriber data and authentication for UE registration",
        lifespan=lifespan,
    )

    app.include_router(auth_router.router)

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok", "service": "udm-ausf", "environment": settings.environment}

    return app


app = create_app()
