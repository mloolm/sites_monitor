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

    # Connection with Monitor
    monitor = relationship("Monitor", back_populates="owner", cascade="all, delete-orphan")
    monitor_by_day = relationship("MonitorByDay", back_populates="owner", cascade="all, delete-orphan")

    # Connection with SSL Monitor
    ssl_monitor = relationship("SSLCertificate", back_populates="owner", cascade="all, delete-orphan")