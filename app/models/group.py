import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.models.debt import Debt
from app.models.user import User


class GroupCreationRequest(BaseModel):
    group_name: str
    description: str = Field(default="")


class GroupBase(GroupCreationRequest):
    model_config = ConfigDict(populate_by_name=True)

    group_id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    working_invites: List[str] = Field(default_factory=list)
    debts: List[Debt] = Field(default_factory=list)


class Group(GroupBase):
    model_config = ConfigDict(populate_by_name=True)

    first_member: User
    members: List[User] = Field(default_factory=list)


class GroupSchema(GroupBase):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    first_member_id: str = Field(alias="first_member")
    members_ids: List[str] = Field(alias="members")
