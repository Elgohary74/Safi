import hashlib
from datetime import datetime, timedelta
from typing import Optional

from app.models import Group, GroupCreationRequest
from app.repositories import NotificationRepository
from app.services.base import BaseService
from app.utils.exceptions import CreationError, ResourceAlreadyExists, ResourceNotFound


class GroupService(BaseService):
    def __init__(self):
        super().__init__()
        self.notification_repo = NotificationRepository()

    def create_new_group(
        self, request: GroupCreationRequest, first_member_id: str
    ) -> Group:
        """
        Creates a new group with the specified details and adds the first member.

        Args:
            request (GroupCreationRequest): An object containing group creation details
                including group_name and description.
            first_member_id (str): The ID of the user to be added as the first member
                and creator of the group.

        Returns:
            Group: A newly created Group object with the first member assigned to both
                the first_member and members fields, with empty working_invites and debts lists.

        Raises:
            Exception: If the user with the given first_member_id does not exist in
                the repository.
        """

        if self.is_user_first_member_of_group_with_name(
            first_member_id, request.group_name
        ):
            raise ResourceAlreadyExists(
                message="Group with this name already exists for the admin"
            )

        first_member = self.user_repo.get_by_id(first_member_id)
        new_group = Group(
            group_name=request.group_name,
            description=request.description,
            first_member=first_member,
            members=[first_member],
            working_invites=[],
            debts=[],
            invite_code="",  # Will be set after group_id is generated
            invite_code_expiry=datetime.now() + timedelta(hours=2),
        )

        new_group.invite_code = self.generate_invite_code(
            first_member_id, new_group.group_id
        )

        return new_group

    def refresh_invite_code(self, admin_id: str, group_id: str) -> str:
        # if not self._is_user_first_member_of_group(admin_id, group_id):
        #     raise CreationError(message="Only the admin can refresh the invite code")

        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        current_expiry = group_schema.invite_code_expiry
        if datetime.now() < current_expiry:
            return group_schema.invite_code

        new_code = self.generate_invite_code(admin_id, group_id)
        new_expiry = datetime.now() + timedelta(hours=2)

        group_schema.invite_code = new_code
        group_schema.invite_code_expiry = new_expiry

        self.group_repo.update(group_id, group_schema)

        return new_code

    def save_new_group(self, new_group: Group) -> str:
        """
        Save a new group to the repository.

        Converts the provided Group object to a schema representation and adds it
        to the group repository.

        Args:
            new_group (Group): The group object to be saved.

        Returns:
            str: The identifier of the newly saved group.
        """
        group_schema = self._convert_group_to_schema(new_group)
        group_id = self.group_repo.add(group_schema)
        if not group_id:
            raise CreationError(message="Failed to create group")
        return group_id

    def generate_invite_code(self, admin_id: str, group_id: str) -> str:
        raw_string = f"{admin_id}{group_id}{datetime.now().timestamp()}"
        return hashlib.sha256(raw_string.encode()).hexdigest()[:8]

    def join_group_by_code(self, user_id: str, invite_code: str) -> Group:
        # find group by code
        group_schema = self.group_repo.get_by_invite_code(invite_code)
        if not group_schema:
            raise ResourceNotFound(message="Invalid invite code")

        group = self._convert_schema_to_group(group_schema)

        # check expiry
        if datetime.now() > group.invite_code_expiry:
            raise CreationError(message="Invite code has expired")

        # check if already member
        if any(member.user_id == user_id for member in group.members):
            raise ResourceAlreadyExists(
                message="User is already a member of this group"
            )

        # add member
        self.group_repo.add_member(group.group_id, user_id)

        # refresh group data
        return self.get_group(group.group_id)

    def get_user_groups(self, user_id: str) -> list[Group]:
        """
        Retrieve all groups associated with a specific user.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            A list of Group objects that the user is a member of.
        """
        group_schemas = self.group_repo.get_groups_by_user(user_id)
        return [
            self._convert_schema_to_group(group_schema)
            for group_schema in group_schemas
        ]

    def _is_user_has_group_with_name(
        self, user_id: str, group_name: str
    ) -> Optional[str]:
        """
        Check if a user has a group with the specified name.

        Args:
            user_id (str): The unique identifier of the user.
            group_name (str): The name of the group to search for.

        Returns:
            Optional[str]: The group ID if a group with the specified name exists
                           for the user, otherwise None.
        """
        groups = self.get_user_groups(user_id)
        for group in groups:
            if group.group_name == group_name:
                return group.group_id
        return None

    def _is_user_first_member_of_group(self, user_id: str, group_id: str) -> bool:
        """
        Check if a user is the first member of a group.

        Args:
            user_id (str): The ID of the user to check.
            group_id (str): The ID of the group to query.

        Returns:
            bool: True if the group exists and the user is the first member of the group,
                  False otherwise.
        """
        group_schema = self.group_repo.get_by_id(group_id)
        return group_schema and group_schema.first_member_id == user_id

    def is_user_first_member_of_group_with_name(
        self, user_id: str, group_name: str
    ) -> bool:
        """
        Check if a user is the first member of a group with the specified name.

        Args:
            user_id (str): The ID of the user to check.
            group_name (str): The name of the group to check.

        Returns:
            bool: True if the user is the first member of the group with the given name,
                  False if the group does not exist or the user is not the first member.
        """
        group_id = self._is_user_has_group_with_name(user_id, group_name)
        if group_id:
            return self._is_user_first_member_of_group(user_id, group_id)
        return False

    def invite_member(self, admin_id: str, group_id: str, email: str):
        # verify admin
        if not self._is_user_first_member_of_group(admin_id, group_id):
            raise CreationError(message="Only the admin can invite members")

        # find user
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ResourceNotFound(message="User with this email does not exist")

        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        # check if already member
        if user.user_id in group_schema.members_ids:
            raise ResourceAlreadyExists(message="User is already a member")

        # check if already pending
        if user.user_id in group_schema.pending_members_ids:
            raise ResourceAlreadyExists(message="User is already invited")

        # add to pending
        self.group_repo.add_pending_member(group_id, user.user_id)

        # Send notification
        from app.models.notification import NotificationSchema

        self.notification_repo = (
            self.notification_repo
            if hasattr(self, "notification_repo")
            else NotificationRepository()
        )

        notification = NotificationSchema(
            user_id=user.user_id,
            message=f"You have been invited to join group '{group_schema.group_name}'",
            type="invite",
            payload={"group_id": group_id, "group_name": group_schema.group_name},
        )
        self.notification_repo.add(notification)

    def respond_to_invite(self, user_id: str, group_id: str, action: str):
        if action not in ["accept", "reject"]:
            raise ValueError("Invalid action")

        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        if user_id not in group_schema.pending_members_ids:
            raise ResourceNotFound(message="No pending invite found for this group")

        if action == "accept":
            self.group_repo.move_pending_to_member(group_id, user_id)
        else:
            self.group_repo.remove_pending_member(group_id, user_id)

    def update_group_info(
        self, admin_id: str, group_id: str, new_name: str, new_description: str
    ):
        if not self._is_user_first_member_of_group(admin_id, group_id):
            raise CreationError(message="Only the admin can update group info")

        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        group_schema.group_name = new_name
        group_schema.description = new_description
        self.group_repo.update(group_id, group_schema)

    def remove_member(self, group_id: str, member_id: str):
        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        if member_id not in group_schema.members_ids:
            raise ResourceNotFound(message="User is not a member of this group")

        self.group_repo.move_member_to_past(group_id, member_id)

    def assign_new_first_member(
        self, current_admin_id: str, group_id: str, new_admin_id: str
    ):
        if not self._is_user_first_member_of_group(current_admin_id, group_id):
            raise CreationError(message="Only the admin can assign a new admin")

        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        if new_admin_id not in group_schema.members_ids:
            raise ResourceNotFound(message="New admin must be a member of the group")

        group_schema.first_member_id = new_admin_id
        self.group_repo.update(group_id, group_schema)

    def leave_group(self, user_id: str, group_id: str, successor_id: str = None):
        group_schema = self.group_repo.get_by_id(group_id)
        if not group_schema:
            raise ResourceNotFound(message="Group not found")

        if user_id not in group_schema.members_ids:
            raise ResourceNotFound(message="User is not a member of this group")

        # admin leaving
        if user_id == group_schema.first_member_id:
            # check if they are the only member
            if len(group_schema.members_ids) == 1:
                # If only member, just leave (group effectively abandoned)
                pass
            else:
                if not successor_id:
                    raise CreationError(
                        message="Admin must assign a new admin before leaving"
                    )
                # Assign new admin
                if successor_id not in group_schema.members_ids:
                    raise CreationError(
                        message="Successor must be a member of the group"
                    )

                group_schema.first_member_id = successor_id
                self.group_repo.update(group_id, group_schema)

        self.group_repo.move_member_to_past(group_id, user_id)
