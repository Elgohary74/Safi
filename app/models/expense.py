import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class Expense:
    description: str
    total_amount: float
    payer_id: str
    group_id: str
    splits: List[Dict] = field(default_factory=list)
    expense_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict:
        return {
            "_id": self.expense_id,
            "description": self.description,
            "total_amount": self.total_amount,
            "payer_id": self.payer_id,
            "group_id": self.group_id,
            "splits": self.splits,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            expense_id=data.get("_id"),
            description=data.get("description"),
            total_amount=data.get("total_amount"),
            payer_id=data.get("payer_id"),
            group_id=data.get("group_id"),
            splits=data.get("splits", []),
            date=data.get("date"),
        )
