import random
import string

from bson.errors import InvalidId

from app.config import get_settings
from app.models.group import Group, GroupCreationRequest
from app.services import GroupService
from app.services.database import MongoDatabase


class GroupController:
    def __init__(self):
        self._db_instance = MongoDatabase()
        self._db = None
        self.group_service = GroupService()

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

    def create_group(
        self, group_request: GroupCreationRequest, first_member_id: str
    ) -> tuple[dict, int]:
        """
        Create a new group with the specified name and add the first member.

        This method validates that the first member (typically the admin) does not already
        have a group with the same name, creates a new group, and persists it to storage.

        Args:
            group_request (GroupCreationRequest): An object containing the group details
                including the group name and other configuration.
            first_member_id (str): The user ID of the first member (admin) of the group.

        Returns:
            tuple: A tuple containing:
                - dict: A response object with:
                    - On success (201): Contains 'message', 'group' (model dump), and 'group_id'
                    - On failure (400): Contains an 'error' message
                - int: HTTP status code (201 for success, 400 for failure)

        Raises:
            None explicitly, but may return 400 error if:
                - A group with the same name already exists for the first member
                - Group creation or persistence fails
        """
        # Check for existing group with the same name for the first member
        if self.group_service.is_user_first_member_of_group_with_name(
            first_member_id, group_request.group_name
        ):
            return {"error": "Group with this name already exists for the admin"}, 400

        # Create new group
        new_group = self.group_service.create_new_group(
            group_request, first_member_id=first_member_id
        )
        group_id = self.group_service.save_new_group(new_group)

        if not group_id:
            return {"error": "Failed to create group"}, 400

        return {
            "message": "Group created successfully",
            "group": new_group.model_dump(),
            "group_id": group_id,
        }, 201

    def get_group_details(self, group_id: str):
        """
        Retrieve the details of a specific group by its ID.

        This method fetches the group information from the group service. If the group
        is not found, it returns an error response with a 404 status code. Otherwise,
        it returns the group's details in a dictionary format with a 200 status code.

        Args:
            group_id (str): The unique identifier of the group to retrieve.

        Returns:
            tuple: A tuple containing a dictionary with either the group details or an
                   error message, and an HTTP status code (200 for success, 404 for not found).
                   - On success: ({"group": group_data}, 200)
                   - On failure: ({"error": "Group not found"}, 404)
        """
        group = self.group_service.get_group(group_id)
        if not group:
            return {"error": "Group not found"}, 404
        return {"group": group.model_dump()}, 200

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
        """
        Retrieve and return a list of groups associated with a specific user.

        This method fetches the groups for the given user ID from the group service,
        serializes each group to a dictionary using model_dump(), and returns them
        in a JSON-compatible response format with a 200 status code.

        Args:
            user_id (str): The unique identifier of the user whose groups are to be retrieved.

        Returns:
            tuple: A tuple containing a dictionary with the key "groups" mapping to a list
                   of group dictionaries, and an HTTP status code of 200.
        """
        groups = self.group_service.get_user_groups(user_id)
        groups = [group.model_dump() for group in groups]
        return {"groups": groups}, 200
