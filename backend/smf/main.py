from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.common.config import get_settings
from backend.common.db import init_db
from backend.smf.routers import session as session_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="SMF Service",
        version="0.1.0",
        description="Session Management Function for PDU session orchestration",
        lifespan=lifespan,
    )

    app.include_router(session_router.router)

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok", "service": "smf", "environment": settings.environment}

    return app


app = create_app()
