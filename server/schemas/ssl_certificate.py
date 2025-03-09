from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SSLCertificate(BaseModel):
    id: int
    site_id: int
    is_ok: bool
    check_dt: datetime
    issuer = str
    valid_from = datetime
    valid_to = datetime

    class Config:
        orm_mode = True