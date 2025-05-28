from pydantic import BaseSettings, PostgresDsn, Field
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    API_2GIS_KEY: Optional[str] = None
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
