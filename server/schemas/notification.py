from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    message: str

class NotificationResponse(NotificationCreate):
    id: int
    sent: bool
    created_at: datetime

    class Config:
        orm_mode = True


class SendMessage(BaseModel):
    message: str