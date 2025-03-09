from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner = relationship("User", back_populates="sites")

    # Связь с таблицей Monitor
    monitor = relationship("Monitor", back_populates="owner", cascade="all, delete-orphan")