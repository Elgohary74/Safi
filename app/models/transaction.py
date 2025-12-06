import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict


@dataclass
class Transaction:
    amount: float
    payer_id: str
    receiver_id: str
    group_id: str
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str

    def to_dict(self) -> Dict:
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
    def from_dict(cls, data: Dict):
        return cls(
            transaction_id=data.get("_id"),
            amount=data.get("amount"),
            payer_id=data.get("payer_id"),
            receiver_id=data.get("receiver_id"),
            group_id=data.get("group_id"),
            date=data.get("date"),
            status=data.get("status"),
        )
