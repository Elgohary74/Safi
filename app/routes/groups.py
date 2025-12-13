from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.controllers.GroupController import GroupController
from app.models import GroupCreationRequest

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")
group_controller = GroupController()


@groups_bp.route("/create", methods=["POST"])
@login_required
def create_group():
    if request.form:
        group_request = GroupCreationRequest(
            group_name=request.form.get("group_name"),
            description=request.form.get("description"),
        )
        result, status_code = group_controller.create_group(
            group_request, current_user.user_id
        )

        if status_code == 201:
            flash("Group created successfully!", "success")
        else:
            flash(result.get("error", "Failed to create group"), "error")

        return redirect(url_for("groups.list_groups", user_id=current_user.user_id))

    data = request.get_json()
    group_request = GroupCreationRequest(
        group_name=data.get("group_name"), description=data.get("description")
    )
    result, status_code = group_controller.create_group(
        group_request, current_user.user_id
    )
    return jsonify(result), status_code


@groups_bp.get("/<string:group_id>/details")
def get_group_details(group_id):
    result, status_code = group_controller.get_group_details(group_id)

    if status_code == 200:
        group = result.get("group", {})

        expenses = []
        members = []
        your_balance = 450  # This should be calculated based on actual data

        return render_template(
            "group_details.html",
            group=group,
            expenses=expenses,
            members=members,
            your_balance=your_balance,
            current_user_id=current_user.user_id,
        )

    # If there's an error, flash it and redirect to groups list
    flash(result.get("error", "Group not found"), "error")
    return redirect(url_for("groups.list_groups", user_id=current_user.user_id))


@groups_bp.post("/<string:group_id>/invite")
def generate_new_invite(group_id):
    user_id = request.json.get("user_id")
    result, status_code = group_controller.generate_new_invite(group_id, user_id)
    return jsonify(result), status_code


@groups_bp.post("/join")
def join_group():
    data = request.get_json()
    invite_code = data.get("invite_code")
    user_id = data.get("user_id")
    result, status_code = group_controller.join_group(invite_code, user_id)
    return jsonify(result), status_code


@groups_bp.delete("/<string:group_id>/members/<string:user_id>")
def remove_member(group_id, user_id):
    requestor_id = request.json.get("requestor_id")
    result, status_code = group_controller.remove_member(
        group_id, user_id, requestor_id
    )
    return jsonify(result), status_code


@groups_bp.get("/list")
@login_required
def list_groups():
    result, status_code = group_controller.list_groups(current_user.user_id)

    if status_code == 200:
        return render_template(
            "groups.html",
            user_id=current_user.user_id,
            groups=result.get("groups", []),
            current_user_id=current_user.user_id,
        )

    return jsonify(result), status_code
