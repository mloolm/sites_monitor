# server/core/config.py
from pydantic_settings import BaseSettings  # Используем новый импорт

class Settings(BaseSettings):
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str
    STAGE: str

    class Config:
        env_file = "core/.env"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@db:3306/{self.DB_DATABASE}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://redis:6379/0"

settings = Settings()




