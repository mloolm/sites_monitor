# models/monitor.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Monitor(Base):
    __tablename__ = "monitor"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    is_ok = Column(Boolean, default=False)
    check_dt = Column(DateTime)  # Timestamp проверки
    code = Column(Integer, index=True)  # Код ответа сайта

    # Связь с таблицей Site
    owner = relationship("Site", back_populates="monitor")