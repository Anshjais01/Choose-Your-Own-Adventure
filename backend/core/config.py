from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os 


class Settings(BaseSettings):
    API_PREFIX: str = '/api'
    DEBUG: bool = False

    DATABASE_URL: str = 'sqlite:///./database.db'

    ALLOWED_ORIGINS: Union[List[str], str] = []

    OPENAI_API_KEY: str = ""

    def __init__(self, **values):
        super().__init__(**values)
        if not self.DEBUG:
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")
            db_name = os.getenv("DB_NAME")
            if db_user and db_password and db_host and db_name:
                self.DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port or 5432}/{db_name}"
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql://", 1)

    @field_validator("API_PREFIX")
    def clean_api_prefix(cls, v: str) -> str:
        if not v:
            return "/api"
        v = v.strip()
        if not v.startswith("/"):
            v = "/" + v
        return v.rstrip("/")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def parse_allowed_origins(cls, v) -> List[str]:
        if isinstance(v, list):
            return [o.strip() for o in v if isinstance(o, str) and o.strip()]
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()