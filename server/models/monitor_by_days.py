from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from db.session import Base

class MonitorByDay(Base):
    __tablename__ = "monitor_by_day"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    uptime = Column(Numeric(precision=5, scale=2), default=False)
    check_dt = Column(DateTime)

    # Connection with Site
    owner = relationship("Site", back_populates="monitor_by_day")