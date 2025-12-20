from typing import Optional

from app.models.group import GroupSchema
from app.utils.exceptions import ResourceNotFound

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
        data = self.collection.find_one({"invite_code": invite_code})
        return GroupSchema.model_validate(data) if data else None

    def add_member(self, group_id: str, user_id: str):
        self.logger.info(f"adding user {user_id} to group {group_id}")
        self.collection.update_one(
            {"_id": group_id}, {"$addToSet": {"members": user_id}}
        )

    def get_groups_by_user(
        self, user_id: str, status: str = "all"
    ) -> list[GroupSchema]:
        self.logger.debug(
            f"fetching groups for user id: {user_id} with status: {status}"
        )

        # Query assuming members is a list of User objects (embedded documents)
        query = {"$or": [{"members": user_id}, {"past_members": user_id}]}

        if status == "active":
            query["is_active"] = True
        elif status == "inactive":
            query["is_active"] = False

        groups = self.collection.find(query)
        return [GroupSchema.model_validate(group) for group in groups]

    def update(self, group_id: str, data: GroupSchema):
        self.collection.update_one(
            {"_id": group_id}, {"$set": data.model_dump(by_alias=True)}
        )

    def delete(self, group_id: str):
        self.collection.delete_one({"_id": group_id})

    def soft_delete(self, group_id: str):
        self.logger.info(f"soft deleting group {group_id}")

        group = self.collection.find_one({"_id": group_id})
        if not group:
            raise ResourceNotFound(message="Group not found")

        current_members = group.get("members", [])

        if current_members:
            result = self.collection.update_one(
                {"_id": group_id},
                {
                    "$set": {"is_active": False, "members": []},
                    "$addToSet": {"past_members": {"$each": current_members}},
                },
            )
            self.logger.info(
                f"Soft delete result (with members): matched={result.matched_count}, modified={result.modified_count}"
            )
        else:
            result = self.collection.update_one(
                {"_id": group_id}, {"$set": {"is_active": False}}
            )
            self.logger.info(
                f"Soft delete result (no members): matched={result.matched_count}, modified={result.modified_count}"
            )

    def add_pending_member(self, group_id: str, user_id: str):
        self.logger.info(f"adding pending user {user_id} to group {group_id}")
        self.collection.update_one(
            {"_id": group_id}, {"$addToSet": {"pending_members": user_id}}
        )

    def remove_pending_member(self, group_id: str, user_id: str):
        self.logger.info(f"removing pending user {user_id} from group {group_id}")
        self.collection.update_one(
            {"_id": group_id}, {"$pull": {"pending_members": user_id}}
        )

    def move_pending_to_member(self, group_id: str, user_id: str):
        self.logger.info(f"moving pending user {user_id} to member in group {group_id}")
        self.collection.update_one(
            {"_id": group_id},
            {"$pull": {"pending_members": user_id}, "$addToSet": {"members": user_id}},
        )

    def move_member_to_past(self, group_id: str, user_id: str):
        self.logger.info(f"moving member {user_id} to past member in group {group_id}")
        self.collection.update_one(
            {"_id": group_id},
            {"$pull": {"members": user_id}, "$addToSet": {"past_members": user_id}},
        )

    def restore(self, group_id: str):
        self.logger.info(f"restoring group {group_id}")

        group = self.collection.find_one({"_id": group_id})
        if not group:
            raise ResourceNotFound(message="Group not found")

        past_members = group.get("past_members", [])

        if past_members:
            self.collection.update_one(
                {"_id": group_id},
                {
                    "$set": {"is_active": True, "past_members": []},
                    "$addToSet": {"members": {"$each": past_members}},
                },
            )
        else:
            self.collection.update_one({"_id": group_id}, {"$set": {"is_active": True}})
