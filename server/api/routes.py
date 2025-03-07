# server/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud import create_site, get_site
from schemas.site import SiteCreate, Site as SiteSchema

router = APIRouter()

@router.post("/add-site/", response_model=SiteSchema)
def create_new_site(site: SiteCreate, db: Session = Depends(get_db)):
    return create_site(db=db, url=site.url)

@router.get("/sites/{site_id}", response_model=SiteSchema)
def read_site(site_id: int, db: Session = Depends(get_db)):
    db_site = get_site(db, site_id=site_id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site

