from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central project configuration loaded from environment variables."""

    project_root: ClassVar[Path] = Path(__file__).resolve().parents[2]

    model_config = SettingsConfigDict(
        env_file=project_root / ".env",
        env_file_encoding="utf-8",
    )

    project_name: str = Field(default="5G Core Management Platform")
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    sqlite_path: Path = Field(default=project_root / "data" / "core.db")

    api_key: str = Field(default="super-secret-admin-key")
    api_key_header: str = Field(default="X-API-Key")

    # Local development URLs (for when running outside Docker)
    udm_ausf_base_url: str = Field(default="http://localhost:8010")
    amf_base_url: str = Field(default="http://localhost:8001")
    smf_base_url: str = Field(default="http://localhost:8005")
    nrf_base_url: str = Field(default="http://localhost:8000")
    nssf_base_url: str = Field(default="http://localhost:8002")
    pcf_base_url: str = Field(default="http://localhost:8003")
    upf_base_url: str = Field(default="http://localhost:8004")
    
    # Management service port
    management_port: int = Field(default=8009)

    @property
    def database_url_async(self) -> str:
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite+aiosqlite:///{self.sqlite_path}"

    @property
    def database_url_sync(self) -> str:
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{self.sqlite_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
