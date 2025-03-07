# server/core/config.py
from pydantic_settings import BaseSettings  # Используем новый импорт

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()





