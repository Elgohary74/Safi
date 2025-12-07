from flask import Blueprint, jsonify, request
from app.controllers.GroupController import GroupController

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")
group_controller = GroupController()


@groups_bp.post("/create")
def create_group():
    data = request.get_json()
    result, status_code = group_controller.create_group(data)
    return jsonify(result), status_code


@groups_bp.get("/<string:group_id>/details")
def get_group_details(group_id):
    result, status_code = group_controller.get_group_details(group_id)
    return jsonify(result), status_code


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
