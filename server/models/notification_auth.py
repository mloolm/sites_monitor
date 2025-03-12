import random
import string
import redis
from db.session import get_db
from sqlalchemy.orm import Session
from core.config import settings
from db.session import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum, ForeignKey
from sqlalchemy.orm import relationship

# Настроим соединение с Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class NotificationAuth(Base):
    __tablename__ = "notification_auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    method = Column(Enum("telegram", "pwa", name="auth_method"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    endpoint = Column(String(255), unique=True, nullable=True)  # chat_id для Telegram или endpoint для PWA
    owner = relationship("User", back_populates="notification_auth")

    @classmethod
    def get_telegram_auth_code(cls, user_id: int) -> str:
        """
        Генерирует случайный код, сохраняет его в Redis и возвращает.
        """
        ttl = 60 * 10  # 15 минут
        # Генерируем случайный 6-значный код
        auth_code = "".join(random.choices(string.ascii_letters + string.digits, k=6))

        # Сохраняем в Redis
        redis_client.setex(auth_code, ttl, user_id)

        return auth_code

    @classmethod
    def check_telegram_auth_code(cls, user_id:int, code:string):
        key = cls.get_telegram_auth_code_key(user_id)

        existing_code = redis_client.get(code)
        if not existing_code:
            return False

        if user_id == existing_code:
            return True

        return False