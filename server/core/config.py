# server/core/config.py
from pydantic_settings import BaseSettings  # Используем новый импорт
from typing import Optional

class Settings(BaseSettings):
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str
    STAGE: str
    SECRET_KEY: str
    CLAIMS_EMAIL: str

    TELEGRAM_BOT_TOKEN: Optional[str] = None

    class Config:
        env_file = "core/.env"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@db:3306/{self.DB_DATABASE}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://redis:6379/0"

    @property
    def ALGORITHM(self) -> str:
        return "HS256"

    @property
    def INTERVAL(self) -> int:
        return 10

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return 60*12

settings = Settings()




