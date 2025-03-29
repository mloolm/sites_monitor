# models/monitor.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from db.session import Base

class SSLCertificate(Base):
    __tablename__ = "ssl_monitor"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    is_ok = Column(Boolean, default=False)
    check_dt = Column(DateTime)  # Timestamp проверки
    issuer = Column(String(255), index=True) #кто выдад
    valid_from = Column(DateTime)
    valid_to = Column(DateTime, index=True)

    # Connection with Site
    owner = relationship("Site", back_populates="ssl_monitor")