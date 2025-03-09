from models.site import Site
from sqlalchemy.orm import Session
from models.user import User
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