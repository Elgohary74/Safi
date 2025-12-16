from typing import Optional

from app.models import Group, GroupCreationRequest, GroupSchema
from app.repositories import GroupRepository, UserRepository
from app.utils.exceptions import CreationError, ResourceAlreadyExists, ResourceNotFound


class GroupService:
    def __init__(self):
        self.group_repo = GroupRepository()
        self.user_repo = UserRepository()

    def _convert_group_to_schema(self, group: Group) -> GroupSchema:
        """
        Converts a Group domain object to its API schema representation.

        This method transforms a Group object into a GroupSchema, extracting relevant
        attributes including group metadata, member identifiers, and financial information.

        Args:
            group (Group): The Group object to be converted.

        Returns:
            GroupSchema: A GroupSchema instance ready for db storage.
        """
        return GroupSchema(
            group_name=group.group_name,
            description=group.description,
            first_member_id=group.first_member.user_id,
            group_id=group.group_id,
            members_ids=[member.user_id for member in group.members],
            working_invites=group.working_invites,
            debts=group.debts,
        )

    def _convert_schema_to_group(self, schema: GroupSchema) -> Group:
        """
        Converts a GroupSchema object to a Group domain object.

        Retrieves the first member and all group members from the user repository
        based on their IDs stored in the schema, then constructs and returns
        a Group instance with the complete member information.

        Args:
            schema (GroupSchema): The group schema object containing group details
                                 and member IDs.

        Returns:
            Group: A Group domain object with all members populated from the
                   user repository.
        """
        first_member = self.user_repo.get_by_id(schema.first_member_id)
        members = [self.user_repo.get_by_id(uid) for uid in schema.members_ids]
        return Group(
            group_name=schema.group_name,
            description=schema.description,
            first_member=first_member,
            group_id=schema.group_id,
            members=members,
            working_invites=schema.working_invites,
            debts=schema.debts,
        )

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
        )
        return new_group

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

    def get_group(self, group_id):
        group_data = self.group_repo.get_by_id(group_id)
        if not group_data:
            raise ResourceNotFound(message="Group not found")
        group = self._convert_schema_to_group(group_data)
        return group
