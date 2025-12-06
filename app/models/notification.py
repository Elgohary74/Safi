import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict


@dataclass
class Notification:
    user_id: str
    message: str
    notification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_read: bool = False

    def to_dict(self) -> Dict:
        return {
            "_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "timestamp": self.timestamp,
            "is_read": self.is_read,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            notification_id=data.get("_id"),
            user_id=data.get("user_id"),
            message=data.get("message"),
            timestamp=data.get("timestamp"),
            is_read=data.get("is_read", False),
        )
