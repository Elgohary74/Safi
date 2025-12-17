from typing import Optional

from app.models.group import GroupSchema

from .base import IRepository


class GroupRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["groups"]

    def add(self, group: GroupSchema) -> str:
        self.logger.info(f"creating group id: {group.group_id}")
        self.collection.insert_one(group.model_dump(by_alias=True))
        return group.group_id

    def get_by_id(self, group_id: str) -> Optional[GroupSchema]:
        self.logger.debug(f"fetching group id: {group_id}")
        data = self.collection.find_one({"_id": group_id})
        return GroupSchema.model_validate(data) if data else None

    def get_by_invite_code(self, invite_code: str) -> Optional[GroupSchema]:
        self.logger.debug(f"searching group by invite code: {invite_code}")
        data = self.collection.find_one({"working_invites": invite_code})
        return GroupSchema.model_validate(data) if data else None

    def add_member(self, group_id: str, user_id: str):
        self.logger.info(f"adding user {user_id} to group {group_id}")
        self.collection.update_one(
            {"_id": group_id}, {"$addToSet": {"members": user_id}}
        )

    def get_groups_by_user(self, user_id: str) -> list[GroupSchema]:
        self.logger.debug(f"fetching groups for user id: {user_id}")
        groups = self.collection.find({"members": user_id})
        return [GroupSchema.model_validate(group) for group in groups]

    def update(self, group_id: str, data: GroupSchema):
        self.collection.update_one(
            {"_id": group_id}, {"$set": data.model_dump(by_alias=True)}
        )

    def delete(self, group_id: str):
        self.collection.delete_one({"_id": group_id})
