from pydantic import BaseModel, HttpUrl

class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str

class PwaSubscribe(BaseModel):
    data: str
