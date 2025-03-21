from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from db.session import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(127), nullable=True)
    message = Column(String(511), nullable=False)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    url = Column(String(511), nullable=True)
