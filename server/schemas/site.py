from pydantic import BaseModel, HttpUrl

class SiteCreate(BaseModel):
    url: HttpUrl

class SiteDelete(BaseModel):
    site_id: int

class Site(BaseModel):
    id: int
    url: str
    is_active: bool

    class Config:
        orm_mode = True

class SiteHealth(BaseModel):
    id: int
    url: str
    is_active: bool
    health: int

    class Config:
        orm_mode = True


