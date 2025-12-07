import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List

from app.models.debt import Debt


@dataclass
class Group:
    group_name: str
    description: str
    admin_id: str
    group_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    members: List[str] = field(default_factory=list)
    working_invites: List[str] = field(default_factory=list)
    debts: List[Debt] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.group_id,
            "group_name": self.group_name,
            "description": self.description,
            "admin_id": self.admin_id,
            "members": self.members,
            "debts": [d.to_dict() for d in self.debts],
            "working_invites": self.working_invites,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        raw_debts = data.get("debts", [])
        return cls(
            group_id=data.get("_id") or str(uuid.uuid4()),
            group_name=data.get("group_name"),
            description=data.get("description"),
            admin_id=data.get("admin_id"),
            members=data.get("members", []),
            working_invites=data.get("working_invites", []),
            debts=[Debt.from_dict(d) for d in raw_debts],
        )
