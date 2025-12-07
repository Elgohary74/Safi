from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Debt:
    from_user: str
    to_user: str
    amount: float
    currency: str = "EGP"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_user": self.from_user,
            "to_user": self.to_user,
            "amount": self.amount,
            "currency": self.currency,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            from_user=data.get("from_user"),
            to_user=data.get("to_user"),
            amount=data.get("amount", 0.0),
            currency=data.get("currency", "EGP"),
        )
