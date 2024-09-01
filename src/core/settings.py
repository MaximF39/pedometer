from functools import lru_cache
from abc import ABC

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class MixinSettings(BaseSettings, ABC):
    """Базовый класс настроек для примеси конфига модели в дочерние классы."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
class ProjectSettings(MixinSettings):
    """Конфигурация проекта."""

    start_command: str = "main:app"
    debug: bool = True
    reload: bool = True
    host: str = "localhost"  # noqa: S104
    port: PositiveInt = 8000

    project_name: str = "Pedometer"
    project_description: str = "Pedometer test"

    project_version: str = "1.7.11"
    docs_url: str = "/api/docs"
    redoc_url: str = "/api/redoc"
    openapi_url: str = "/api/openapi.json"

    metrics_endpoint: str = "/metrics"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


settings = ProjectSettings()
