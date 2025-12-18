from flask import flash, redirect, render_template, request, url_for
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models.group import GroupCreationRequest
from app.services import GroupService


class GroupController(BaseController):
    route_prefix = "/groups"

    def __init__(self):
        super().__init__()
        self.group_service = GroupService()

    @route("/create", methods=["POST"])
    def create_group(self):
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
        group_request = GroupCreationRequest(**request.form.to_dict())
        new_group = self.group_service.create_new_group(
            group_request, first_member_id=self.current_user.user_id
        )
        self.group_service.save_new_group(new_group)

        flash("Group created successfully!", "success")

        return redirect(url_for("GroupController:list_groups"))

    @route("/<string:group_id>/details", methods=["GET"])
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
        return render_template(
            "group_details.html",
            group=group.model_dump(),
            expenses=[],
            members=[],
            your_balance=450,
            current_user_id=self.current_user.user_id,
        )

    @route("/list", methods=["GET"])
    def list_groups(self):
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
        groups = self.group_service.get_user_groups(self.current_user.user_id)
        groups = [group.model_dump() for group in groups]
        return render_template(
            "groups.html",
            user_id=self.current_user.user_id,
            groups=groups,
            current_user_id=self.current_user.user_id,
        )
