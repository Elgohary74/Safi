from typing import Optional

from app.models.group import Group

from .base import IRepository


class GroupRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["groups"]

    def add(self, group: Group) -> str:
        self.logger.info(f"creating group: {group.group_name}")
        self.collection.insert_one(group.to_dict())
        return group.group_id

    def get_by_id(self, group_id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": group_id})

    def get_by_invite_code(self, invite_code: str) -> Optional[dict]:
        self.logger.debug(f"searching group by invite code: {invite_code}")
        return self.collection.find_one({"invites": invite_code})

    def add_member(self, group_id: str, user_id: str):
        self.logger.info(f"adding user {user_id} to group {group_id}")
        self.collection.update_one(
            {"_id": group_id}, {"$addToSet": {"members": user_id}}
        )

    def update(self, group_id: str, data: dict):
        self.collection.update_one({"_id": group_id}, {"$set": data})

    def delete(self, group_id: str):
        self.collection.delete_one({"_id": group_id})
