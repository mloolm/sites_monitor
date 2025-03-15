from models.site import Site
from sqlalchemy.orm import Session
from models.user import User
from models.notification_auth import NotificationAuth
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_user(db: Session, login: str, password: str) -> User:
    user = User(login=login)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_login(db: Session, login: str) -> Optional[User]:
    return db.query(User).filter(User.login == login).first()

def authenticate_user(db: Session, login: str, password: str) -> Optional[User]:
    user = get_user_by_login(db, login)
    if not user or not user.verify_password(password):
        return None
    return user

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_site(db: Session, user: User, site_id: int):
    return db.query(Site).filter(Site.id == site_id, Site.user_id == user.id).first()


def create_site(db: Session, user: User, url: str):
    db_site = Site(url=url, user_id=user.id)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

def get_sites(db: Session, user: User):
    return db.query(Site).filter(Site.user_id == user.id)

from datetime import datetime, timedelta
from sqlalchemy import text

def get_sites_health(db: Session, sites):
    site_ids = [site.id for site in sites]

    # Определяем дату начала последней недели
    last_week = datetime.utcnow() - timedelta(days=7)

    # SQL-запрос для подсчета проверок и доступности
    sql = text("""
        SELECT 
            site_id, 
            COUNT(*) as total_checks, 
            SUM(CASE WHEN is_ok THEN 1 ELSE 0 END) as successful_checks 
        FROM 
            monitor 
        WHERE 
            site_id IN :site_ids 
            AND check_dt > :last_week 
        GROUP BY 
            site_id
    """)

    # Выполняем запрос
    result = db.execute(sql, {"site_ids": tuple(site_ids), "last_week": last_week}).fetchall()

    # Подсчитываем процент доступности для каждого сайта
    health_data = {}
    for row in result:
        site_id = row.site_id
        total_checks = row.total_checks
        successful_checks = row.successful_checks
        availability_percentage = round((successful_checks / total_checks * 100)) if total_checks > 0 else 0

        health_data[site_id] = availability_percentage

    return health_data



def delete_site(db: Session, user: User, site_id: int):
    site = get_site(db, user, site_id)
    if site:
        db.delete(site)  # Удалить
        db.commit()  # Подтвердить изменения
        return True
    return False  # Если сайт не найден

def get_user_noty_providers(db: Session, user: User):
    providers = db.query(NotificationAuth).filter(NotificationAuth.user_id == user.id).all()
    return providers