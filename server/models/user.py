from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(32), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Для токенов (если используете stateless JWT, эти поля могут не понадобиться)
    token = Column(String(255), unique=True)
    token_expires = Column(DateTime(timezone=True))

    # Связь с таблицей sites
    sites = relationship("Site", back_populates="owner")

    notification_auth = relationship("NotificationAuth", back_populates="owner")

    # Методы для работы с паролями
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str) -> None:
        self.hashed_password = pwd_context.hash(password)