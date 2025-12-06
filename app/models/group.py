import uuid
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Group:
    group_name: str
    description: str
    admin_id: str
    group_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    members: List[str] = field(default_factory=list)
    debts: List[dict] = field(default_factory=list)
    working_invites: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "_id": self.group_id,
            "group_name": self.group_name,
            "description": self.description,
            "admin_id": self.admin_id,
            "members": self.members,
            "debts": self.debts,
            "working_invites": self.working_invites,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            group_id=data.get("_id"),
            group_name=data.get("group_name"),
            description=data.get("description"),
            admin_id=data.get("admin_id"),
            members=data.get("members", []),
            debts=data.get("debts", []),
            working_invites=data.get("working_invites", []),
        )
