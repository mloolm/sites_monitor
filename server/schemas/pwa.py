from pydantic import BaseModel, HttpUrl
from typing import Optional

class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str

class PwaSubscribe(BaseModel):
    data: str
