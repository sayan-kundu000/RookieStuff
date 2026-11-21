import os
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for RookieStuff."""

    # Project metadata
    app_name: str = "RookieStuff"
    version: str = "0.1.0"
    environment: str = "development"

    # API Keys & External Services
    github_token: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Persistence / LangGraph Checkpoints
    checkpointer_type: Literal["memory", "sqlite"] = "memory"
    sqlite_db_path: str = "checkpoints.db"

    # Linter & Sandbox Configuration
    linter_timeout: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
