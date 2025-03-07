from sqlalchemy.orm import Session
from models.site import Site


def get_site(db: Session, site_id: int):
    return db.query(Site).filter(Site.id == site_id).first()


def create_site(db: Session, url: str):
    db_site = Site(url=url)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

def get_sites(db: Session):
    return db.query(Site).all()