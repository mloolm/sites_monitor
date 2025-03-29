import random
import string
import redis
from core.config import settings
from db.session import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
import hashlib


# Настроим соединение с Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class NotificationAuth(Base):
    __tablename__ = "notification_auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    method = Column(Enum("telegram", "pwa", name="auth_method"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    endpoint = Column(Text, nullable=True)
    endpoint_hash = Column(String(127), nullable=False, index=True)
    owner = relationship("User", back_populates="notification_auth")

    @classmethod
    def get_telegram_auth_code(cls, user_id: int) -> str:
        """
        Generates a random code, saves it in Redis, and returns it.
        """
        ttl = 60 * 10  # 15 минут
        # Generates a random 6-digit code.
        auth_code = "".join(random.choices(string.ascii_letters + string.digits, k=6))

        # Saves it in Redis.
        redis_client.setex(auth_code, ttl, user_id)

        return auth_code

    @classmethod
    def check_telegram_auth_code(cls, code:string):

        existing_code_for_user = redis_client.get(code)
        if not existing_code_for_user:
            return False

        return existing_code_for_user

    @classmethod
    def get_telegram_webhook_url_hash(cls):
        if not settings.TELEGRAM_BOT_TOKEN:
            return False

        hash_object = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode('utf-8'))
        hash_hex = hash_object.hexdigest()

        return hash_hex

    @classmethod
    def get_endpoint_hash(cls, endpoint: str):
        hash_object = hashlib.sha256(endpoint.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        return hash_hex
