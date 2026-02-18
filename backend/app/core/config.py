import os
from pathlib import Path

from typing import Any, List, Optional, Annotated
from pydantic import (
    AnyUrl,
    AnyHttpUrl,
    EmailStr,
    PostgresDsn,
    ValidationInfo,
    field_validator,
    BeforeValidator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", str(Path(__file__).resolve().parents[3] / ".env")),
        env_file_encoding="utf-8"
    )
    
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"

    TEST_POSTGRES_DB: str = "appdb_test"
    TEST_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/appdb_test"

    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_USERNAME: str
    PROJECT_NAME: str

    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        host = info.data.get("POSTGRES_SERVER")
        db = info.data.get("POSTGRES_DB")

        if all([user, password, host, db]):
            return f"postgresql://{user}:{password}@{host}/{db}"
        return None

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and v:
            return [i.strip().strip('"').strip("'") for i in v.strip("[]").split(",")]
        elif isinstance(v, list):
            return v
        return []


settings = Settings()  # type: ignore
