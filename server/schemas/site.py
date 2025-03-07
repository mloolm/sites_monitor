from pydantic import BaseModel

class SiteCreate(BaseModel):
    url: str

class Site(BaseModel):
    id: int
    url: str
    is_active: bool

    class Config:
        orm_mode = True