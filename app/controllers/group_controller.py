from flask import flash, redirect, render_template, request, url_for
from flask_classful import route
from flask_login import current_user

from app.controllers.base_controller import BaseController
from app.models.group import GroupCreationRequest
from app.services import ExpenseService, GroupService
from app.utils.exceptions import CreationError, ResourceAlreadyExists, ResourceNotFound


class GroupController(BaseController):
    route_prefix = "/groups"

    def __init__(self):
        super().__init__()
        self.group_service = GroupService()
        self.expense_service = ExpenseService()

    @route("/create", methods=["POST"])
    def create_group(self):
        group_request = GroupCreationRequest(**request.form.to_dict())
        new_group = self.group_service.create_new_group(
            group_request, first_member_id=self.current_user.user_id
        )
        self.group_service.save_new_group(new_group)

        flash("Group created successfully!", "success")
        return redirect(url_for("GroupController:list_groups"))

    @route("/join", methods=["POST"])
    def join_group(self):
        invite_code = request.form.get("invite_code")
        try:
            self.group_service.join_group_by_code(
                self.current_user.user_id, invite_code
            )
            flash("Joined group successfully!", "success")
        except (ResourceNotFound, CreationError, ResourceAlreadyExists) as e:
            flash(e.message, "danger")

        return redirect(url_for("GroupController:list_groups"))

    @route("/<group_id>/invite", methods=["POST"])
    def invite_member(self, group_id):
        email = request.form.get("email")
        try:
            self.group_service.invite_member(self.current_user.user_id, group_id, email)
            flash("Invitation sent successfully!", "success")
        except (ResourceNotFound, CreationError, ResourceAlreadyExists) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:get_group_details", group_id=group_id))

    @route("/<group_id>/respond", methods=["POST"])
    def respond_to_invite(self, group_id):
        action = request.form.get("action")
        try:
            self.group_service.respond_to_invite(
                self.current_user.user_id, group_id, action
            )
            flash(f"Invitation {action}ed!", "success")
        except (ResourceNotFound, ValueError) as e:
            if hasattr(e, "message"):
                flash(e.message, "danger")
            else:
                flash(str(e), "danger")
        return redirect(url_for("GroupController:list_groups"))

    @route("/<group_id>/leave", methods=["POST"])
    def leave_group(self, group_id):
        try:
            self.group_service.leave_group(self.current_user.user_id, group_id)
            flash("You have left the group.", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:list_groups"))

    @route("/<string:group_id>/details", methods=["GET"])
    def get_group_details(self, group_id: str):
        group = self.group_service.get_group(group_id)
        expenses = self.expense_service.get_group_expenses(group_id)

        return render_template(
            "group_details.html",
            group=group.model_dump(),
            expenses=expenses,
            members=[],
            your_balance=-100,
        )

    @route("/list", methods=["GET"])
    def list_groups(self):
        user_id = current_user.user_id
        groups = self.group_service.get_user_groups(user_id)
        groups = [group.model_dump() for group in groups]

        return render_template(
            "groups.html",
            groups=groups,
        )
