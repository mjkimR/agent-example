import functools
import os

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib


def get_repo_path():
    """Get the path to the repository."""
    path = str(pathlib.Path(__file__).parent.parent.parent.parent.resolve())
    return path


def get_app_path():
    """Get the path to the app directory."""
    path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
    return path


def get_env_filename():
    runtime_env = os.getenv("ENV")
    home = get_repo_path()

    return f"{home}/.env.{runtime_env}" if runtime_env else f"{home}/.env"


if os.path.exists(get_env_filename()):
    from dotenv import load_dotenv

    load_dotenv(get_env_filename())


class AppSettings(BaseSettings):
    DATABASE_URL: str = Field(default=f"sqlite+aiosqlite:///{get_repo_path()}/.test.db")

    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        validate_assignment=True,
        extra="ignore",
    )


class VectorDBSettings(BaseSettings):
    KIND: str = Field(default="qdrant")
    URL: str = Field(default="http://localhost:6333")
    API_KEY: SecretStr = Field()

    model_config = SettingsConfigDict(
        env_prefix="VECTOR_DB_",
        env_ignore_empty=True,
        validate_assignment=True,
        extra="ignore",
    )


@functools.lru_cache
def get_app_settings():
    return AppSettings()  # type: ignore


@functools.lru_cache
def get_vector_db_settings():
    return VectorDBSettings()  # type: ignore
