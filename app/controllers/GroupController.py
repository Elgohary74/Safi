import random
import string
from typing import Any, Dict

from bson.errors import InvalidId

from app.config import get_settings
from app.models.group import Group
from app.services.database import MongoDatabase


class GroupController:
    def __init__(self):
        self._db_instance = MongoDatabase()
        self._db = None

    @property
    def db(self):
        """Lazy initialization of database connection"""
        if self._db is None:
            self._db = self._db_instance.get_db()
        return self._db

    @classmethod
    def generate_invite_code(cls) -> str:
        settings = get_settings()
        length = settings.INVITE_CODE_LENGTH
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def create_group(self, data: Dict[str, Any]):
        required_fields = ["group_name", "description", "admin_id"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        # Check if admin already has a group with the same name
        existing_group = self.db.groups.find_one(
            {"group_name": data["group_name"], "admin_id": data["admin_id"]}
        )
        if existing_group:
            return {"error": "Group with this name already exists for the admin"}, 400

        # Create new group
        group = Group(
            group_name=data["group_name"],
            description=data["description"],
            admin_id=data["admin_id"],
        )
        group.members.append(data["admin_id"])
        self.db.groups.insert_one(group.to_dict())

        return {
            "message": "Group created successfully",
            "group": group.to_dict(),
            "group_id": group.group_id,
        }, 201

    def get_group_details(self, group_id: str):
        try:
            group_data = self.db.groups.find_one({"_id": group_id})
            if not group_data:
                return {"error": "Group not found"}, 404

            group = Group.from_dict(group_data)
            return {"group": group.to_dict()}, 200
        except InvalidId:
            return {"error": "Invalid group ID format"}, 400

    def generate_new_invite(self, group_id: str, user_id: str):
        try:
            group_data = self.db.groups.find_one({"_id": group_id})
            if not group_data:
                return {"error": "Group not found"}, 404

            if not user_id or user_id != group_data["admin_id"]:
                return {"error": "Only group admin can generate invite codes"}, 403

            invite_code = self.generate_invite_code()
            self.db.groups.update_one(
                {"_id": group_id}, {"$push": {"working_invites": invite_code}}
            )

            return {
                "message": "New invite code generated",
                "invite_code": invite_code,
            }, 200
        except InvalidId:
            return {"error": "Invalid group ID format"}, 400

    def join_group(self, invite_code: str, user_id: str):
        if not invite_code or not user_id:
            return {"error": "Missing invite_code or user_id"}, 400

        group_data = self.db.groups.find_one({"working_invites": invite_code})
        if not group_data:
            return {"error": "Invalid or expired invite code"}, 404

        group = Group.from_dict(group_data)
        if user_id in group.members:
            return {"message": "User is already a member of this group"}, 200

        self.db.groups.update_one(
            {"_id": group.group_id}, {"$addToSet": {"members": user_id}}
        )

        return {
            "message": "Successfully joined the group",
            "group": {"group_id": group.group_id, "group_name": group.group_name},
        }, 200

    def remove_member(self, group_id: str, user_id: str, requestor_id: str):
        try:
            group_data = self.db.groups.find_one({"_id": group_id})
            if not group_data:
                return {"error": "Group not found"}, 404

            group = Group.from_dict(group_data)
            if not requestor_id or (
                requestor_id != group.admin_id and requestor_id != user_id
            ):
                return {"error": "Unauthorized to remove this member"}, 403

            if user_id == group.admin_id:
                return {"error": "Cannot remove the group admin"}, 400

            if user_id in group.members:
                self.db.groups.update_one(
                    {"_id": group_id}, {"$pull": {"members": user_id}}
                )
                return {"message": "Member removed successfully"}, 200
            else:
                return {"error": "User is not a member of this group"}, 404
        except InvalidId:
            return {"error": "Invalid group ID format"}, 400

    def list_groups(self, user_id: str):
        if not user_id:
            return {"error": "Missing user_id"}, 400

        groups_cursor = self.db.groups.find({"members": user_id})
        groups = [
            {
                "group_id": group_data["_id"],
                "group_name": group_data["group_name"],
                "description": group_data["description"],
                "admin_id": group_data["admin_id"],
            }
            for group_data in groups_cursor
        ]

        return {"groups": groups}, 200
