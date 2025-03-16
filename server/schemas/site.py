from datetime import datetime
from typing import Union
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
    ssl: Union[datetime, None]

    class Config:
        orm_mode = True


