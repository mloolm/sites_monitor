from pydantic import BaseModel

class SiteCreate(BaseModel):
    url: str

class SiteDelete(BaseModel):
    site_id: int

class Site(BaseModel):
    id: int
    url: str
    is_active: bool

    class Config:
        orm_mode = True