"""Application configuration via environment variables."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Zenith Dynamic Hotel Pricing Engine"
    API_V1_STR: str = "/api/v1"

    # Database — default to SQLite for development & testing;
    # production should use PostgreSQL via DATABASE_URL env var.
    DATABASE_URL: str = "sqlite+aiosqlite:///./zenith_hotel.db"

    # Redis (optional — falls back to in-memory cache)
    REDIS_URL: Optional[str] = None
    CACHE_DEFAULT_TTL: int = 300  # seconds

    # Environment
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
