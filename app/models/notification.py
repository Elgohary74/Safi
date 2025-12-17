import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.models.user import User


class NotificationBase(BaseModel):
    notification_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    is_read: bool = Field(default=False)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    type: str = Field(default="generic")
    payload: dict = Field(default_factory=dict)


class Notification(NotificationBase):
    user: User


class NotificationSchema(NotificationBase):
    user_id: str
