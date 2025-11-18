from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.amf.routers import ue as ue_router
from backend.common.config import get_settings
from backend.common.db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="AMF Service",
        version="0.1.0",
        description="Access and Mobility Management Function for UE registration",
        lifespan=lifespan,
    )
    app.include_router(ue_router.router)

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok", "service": "amf", "environment": settings.environment}

    return app


app = create_app()
