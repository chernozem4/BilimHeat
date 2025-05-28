from pydantic import BaseSettings, PostgresDsn, Field, validator
from typing import Optional


class Settings(BaseSettings):
    """Конфигурация проекта с загрузкой из .env."""

    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    API_2GIS_KEY: Optional[str] = Field(default=None, env="API_2GIS_KEY")

    DEBUG: bool = Field(default=False, env="DEBUG")

    @validator("JWT_SECRET_KEY")
    def validate_jwt_secret_length(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY должен быть минимум 32 символа")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
