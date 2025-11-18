from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central project configuration loaded from environment variables."""

    project_root = Path(__file__).resolve().parents[2]

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

    udm_ausf_base_url: str = Field(default="http://udm-ausf:8010")
    amf_base_url: str = Field(default="http://amf:8001")
    smf_base_url: str = Field(default="http://smf:8005")
    nrf_base_url: str = Field(default="http://nrf:8000")
    nssf_base_url: str = Field(default="http://nssf:8002")
    pcf_base_url: str = Field(default="http://pcf:8003")
    upf_base_url: str = Field(default="http://upf:8004")

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
