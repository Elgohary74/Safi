from app.models.group import GroupCreationRequest
from app.services import GroupService


class GroupController:
    def __init__(self):
        self.group_service = GroupService()

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
