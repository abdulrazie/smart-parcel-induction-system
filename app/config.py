"""
Application Configuration Module
--------------------------------
This module uses Pydantic's `BaseSettings` to manage application configuration.

Key Concepts:
1. Environment Separation: Secrets and URLs are loaded from a `.env` file or the OS environment.
   They are NEVER hardcoded into source code.
2. Type Validation: Pydantic automatically validates types (e.g. converting "True" string to boolean).
3. Caching: The `get_settings()` function uses `@lru_cache` to avoid re-reading `.env` on every call.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central settings model for the Smart Parcel Induction System.
    Default values are provided, but any variable present in .env will override them.
    """
    # General App Settings
    APP_NAME: str = "Smart Parcel Induction System"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Database Settings
    # Format: postgresql://<user>:<password>@<host>:<port>/<db_name>
    # Or SQLite: sqlite:///./mailroom_dev.db
    DATABASE_URL: str = "sqlite:///./mailroom_dev.db"

    # Tell Pydantic to read from a .env file if available
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore unexpected variables in .env without raising an error
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings object.
    Using @lru_cache ensures the settings file is parsed once, improving performance.
    """
    return Settings()
