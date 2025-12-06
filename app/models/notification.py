import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class Notification:
    user_id: str
    message: str
    is_read: bool = field(default=False)
    notification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "timestamp": self.timestamp,
            "is_read": self.is_read,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            notification_id=data.get("_id") or str(uuid.uuid4()),
            user_id=data.get("user_id"),
            message=data.get("message"),
            timestamp=data.get("timestamp") or datetime.now(timezone.utc),
            is_read=data.get("is_read", False),
        )
