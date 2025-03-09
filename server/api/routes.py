# server/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud import create_site, get_site, get_sites, get_user_by_login
from schemas.site import SiteCreate, Site as SiteSchema
from schemas.user import User as UserSchema
from typing import List
from .auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Применяем ко всем маршрутам
)

@router.get("/user-data", response_model=UserSchema)
def get_user_data(
    current_user: str = Depends(get_current_user),  # Получаем текущего пользователя
    db: Session = Depends(get_db)
):
    """
    Возвращает информацию о текущем пользователе.
    """
    if current_user:
        return current_user
    else:
        raise HTTPException(status_code=401, detail="User not authorised")


@router.post("/add-site", response_model=SiteSchema)
def create_new_site(site: SiteCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_site(db=db, user=current_user, url=site.url)

@router.get("/sites/", response_model=List[SiteSchema])
def sites_list(db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """
        Возвращает список всех сайтов.
        """
    sites = get_sites(db, current_user)
    if not sites:
        raise HTTPException(status_code=404, detail="No sites found")

    return sites
    #return [{"id": site.id, "url": site.url} for site in sites]
@router.get("/sites/{site_id}", response_model=SiteSchema)
def read_site(site_id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    db_site = get_site(db, user=current_user, site_id=site_id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site

