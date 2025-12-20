from flask import flash, redirect, render_template, request, session, url_for
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models.group import GroupCreationRequest
from app.services import ExpenseService, GroupService
from app.utils.decorators import require_group_admin
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
            flash(e.message, "error")

        return redirect(url_for("GroupController:list_groups"))

    @route("/<group_id>/invite", methods=["POST"])
    @require_group_admin
    def invite_member(self, group_id):
        email = request.form.get("email")
        try:
            self.group_service.invite_member(self.current_user.user_id, group_id, email)
            flash("Invitation sent successfully!", "success")
        except (ResourceNotFound, CreationError, ResourceAlreadyExists) as e:
            flash(e.message, "error")
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

    @route("/<group_id>/invite/refresh", methods=["POST"])
    @require_group_admin
    def refresh_invite_code(self, group_id):
        try:
            self.group_service.refresh_invite_code(self.current_user.user_id, group_id)
            flash("Invite code regenerated successfully!", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:get_group_details", group_id=group_id))

    @route("/<group_id>/leave", methods=["POST"])
    def leave_group(self, group_id):
        successor_id = request.form.get("successor_id")
        try:
            self.group_service.leave_group(
                self.current_user.user_id, group_id, successor_id
            )
            flash("You have left the group.", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
            return redirect(
                url_for("GroupController:get_group_details", group_id=group_id)
            )
        return redirect(url_for("GroupController:list_groups"))

    @route("/<group_id>/update", methods=["POST"])
    @require_group_admin
    def update_group(self, group_id):
        new_name = request.form.get("new_group_name")
        new_description = request.form.get("new_group_description")
        try:
            self.group_service.update_group_info(group_id, new_name, new_description)
            flash("Group updated successfully!", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:get_group_details", group_id=group_id))

    @route("/<group_id>/members/remove", methods=["POST"])
    @require_group_admin
    def remove_member(self, group_id):
        member_id = request.form.get("member_id")
        try:
            self.group_service.remove_member(group_id, member_id)
            flash("Member removed successfully!", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:get_group_details", group_id=group_id))

    @route("/<group_id>/assign_admin", methods=["POST"])
    @require_group_admin
    def assign_admin(self, group_id):
        new_admin_id = request.form.get("new_admin_id")
        try:
            self.group_service.assign_new_first_member(
                self.current_user.user_id, group_id, new_admin_id
            )
            flash("Admin privileges transferred successfully!", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:get_group_details", group_id=group_id))

    @route("/<string:group_id>/details", methods=["GET"])
    def get_group_details(self, group_id: str):
        group = self.group_service.get_group(group_id)
        expenses = self.expense_service.get_group_expenses(group_id)

        user_shares = []
        for expense in expenses:
            involved_users = [split.participant.user_id for split in expense.splits]
            if self.current_user.user_id not in involved_users:
                user_shares.append(0.0)
                continue

            share = -expense.total_amount / len(expense.splits)
            if expense.payer.user_id == self.current_user.user_id:
                share += expense.total_amount
            user_shares.append(round(share, 2))

        is_admin = False
        if group.first_member.user_id == self.current_user.user_id:
            self.group_service.refresh_invite_code(self.current_user.user_id, group_id)
            is_admin = True

        # determining back endpoint logic
        # if the user came from dashboard or groups list, store that preference
        if request.referrer:
            if "dashboard" in request.referrer:
                session[f"return_to_{group_id}"] = "dashboard.dashboard_index"
            elif "groups/list" in request.referrer:
                session[f"return_to_{group_id}"] = "GroupController:list_groups"

        # default to groups list if nothing stored or known
        back_endpoint = session.get(
            f"return_to_{group_id}", "GroupController:list_groups"
        )

        return render_template(
            "group_details.html",
            group=group,
            expenses=list(zip(expenses, user_shares)),
            your_balance=round(sum(user_shares), 2),
            current_user=self.current_user,
            is_admin=is_admin,
            back_endpoint=back_endpoint,
        )

    @route("/list", methods=["GET"])
    def list_groups(self):
        user_id = self.current_user.user_id
        # Always fetch all groups for client-side filtering
        groups = self.group_service.get_user_groups(user_id, status="all")
        groups = [group for group in groups]

        # sort groups by active first then alphabetically
        groups.sort(key=lambda group: (not group.is_active, group.group_name))

        return render_template(
            "groups.html",
            groups=groups,
            current_user=self.current_user,
        )

    @route("/<group_id>/members", methods=["GET"])
    def get_group_members(self, group_id):
        group = self.group_service.get_group(group_id)
        if not group:
            raise ResourceNotFound("Group not found.")

        members = [
            {"user_id": member.user_id, "name": member.name} for member in group.members
        ]
        return {"members": members}

    @require_group_admin
    @route("/<group_id>/delete", methods=["POST"])
    def delete_group(self, group_id: str):
        try:
            self.group_service.delete_group(group_id)
            flash("Group deleted successfully!", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
            return redirect(
                url_for("GroupController:get_group_details", group_id=group_id)
            )
        return redirect(url_for("GroupController:list_groups"))

    @require_group_admin
    @route("/<group_id>/restore", methods=["POST"])
    def restore_group(self, group_id: str):
        try:
            self.group_service.restore_group(self.current_user.user_id, group_id)
            flash("Group restored successfully!", "success")
        except (ResourceNotFound, CreationError) as e:
            flash(e.message, "danger")
        return redirect(url_for("GroupController:get_group_details", group_id=group_id))
