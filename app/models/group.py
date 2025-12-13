import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.models.debt import Debt
from app.models.user import User


class GroupCreationRequest(BaseModel):
    group_name: str
    description: str = Field(default="")


class Group(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    group_name: str
    description: str
    first_member: User
    group_id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    members: List[User] = Field(default_factory=list)
    working_invites: List[str] = Field(default_factory=list)
    debts: List[Debt] = Field(default_factory=list)


class GroupSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    group_name: str
    description: str
    first_member_id: str = Field(alias="first_member")
    group_id: str = Field(alias="_id")
    members_ids: List[str] = Field(alias="members")
    working_invites: List[str]
    debts: List[Debt]
