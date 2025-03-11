from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Enum
from db.session import Base

class NotificationAuth(Base):
    __tablename__ = "notification_auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    method = Column(Enum("telegram", "pwa", name="auth_method"), nullable=False)
    hash_code = Column(String(63), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    endpoint = Column(String(255), unique=True, nullable=True)  # chat_id для Telegram или endpoint для PWA
