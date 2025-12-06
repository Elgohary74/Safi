import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class Transaction:
    amount: float
    payer_id: str
    receiver_id: str
    group_id: str
    status: str = field(default="pending")
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.transaction_id,
            "amount": self.amount,
            "payer_id": self.payer_id,
            "receiver_id": self.receiver_id,
            "group_id": self.group_id,
            "date": self.date,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            transaction_id=data.get("_id") or str(uuid.uuid4()),
            amount=data.get("amount", 0.0),
            payer_id=data.get("payer_id"),
            receiver_id=data.get("receiver_id"),
            group_id=data.get("group_id"),
            date=data.get("date") or datetime.now(timezone.utc),
            status=data.get("status", "pending"),
        )
