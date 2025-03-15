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