from sqlalchemy import Column, Integer, String, DateTime, Boolean
from db.session import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime)
    # Добавьте нужные поля