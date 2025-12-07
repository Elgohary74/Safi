import random
import string

from bson.errors import InvalidId
from flask import Blueprint, request, jsonify

from app.config import get_settings
from app.models.group import Group
from app.services.database import MongoDatabase

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


def generate_invite_code():
    settings = get_settings()
    length = settings.INVITE_CODE_LENGTH
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@groups_bp.post("/create")
def create_group():
    data = request.get_json()

    required_fields = ["group_name", "description", "admin_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # verify that this admin has no existing group with the same name
    db = MongoDatabase().get_db()
    existing_group = db.groups.find_one(
        {"group_name": data["group_name"], "admin_id": data["admin_id"]}
    )
    if existing_group:
        return (
            jsonify({"error": "Group with this name already exists for the admin"}),
            400,
        )

    # create new group
    group = Group(
        group_name=data["group_name"],
        description=data["description"],
        admin_id=data["admin_id"],
    )
    group.members.append(data["admin_id"])
    db.groups.insert_one(group.to_dict())

    return (
        jsonify(
            {
                "message": "Group created successfully",
                "group": group.to_dict(),
                "group_id": group.group_id,
            }
        ),
        201,
    )


@groups_bp.get("/<string:group_id>/details")
def get_group_details(group_id):
    try:
        db = MongoDatabase().get_db()
        group_data = db.groups.find_one({"_id": group_id})
        if not group_data:
            return jsonify({"error": "Group not found"}), 404

        group = Group.from_dict(group_data)
        return jsonify({"group": group.to_dict()})
    except InvalidId:
        return jsonify({"error": "Invalid group ID format"}), 400


@groups_bp.post("/<string:group_id>/invite")
def generate_new_invite(group_id):
    try:
        db = MongoDatabase().get_db()
        group_data = db.groups.find_one({"_id": group_id})
        if not group_data:
            return jsonify({"error": "Group not found"}), 404

        # Verify if user is admin
        user_id = request.json.get("user_id")
        if not user_id or user_id != group_data["admin_id"]:
            return jsonify({"error": "Only group admin can generate invite codes"}), 403

        # Generate new invite code
        invite_code = generate_invite_code()

        # Add to working_invites array
        db.groups.update_one(
            {"_id": group_id}, {"$push": {"working_invites": invite_code}}
        )

        return jsonify(
            {"message": "New invite code generated", "invite_code": invite_code}
        )
    except InvalidId:
        return jsonify({"error": "Invalid group ID format"}), 400


@groups_bp.post("/join")
def join_group():
    """Join a group using invite code"""
    data = request.get_json()

    if not data.get("invite_code") or not data.get("user_id"):
        return jsonify({"error": "Missing invite_code or user_id"}), 400

    invite_code = data["invite_code"]
    user_id = data["user_id"]

    db = MongoDatabase().get_db()
    group_data = db.groups.find_one({"working_invites": invite_code})
    if not group_data:
        return jsonify({"error": "Invalid or expired invite code"}), 404

    group = Group.from_dict(group_data)
    if user_id in group.members:
        return jsonify({"message": "User is already a member of this group"}), 200

    db.groups.update_one({"_id": group.group_id}, {"$addToSet": {"members": user_id}})

    return jsonify(
        {
            "message": "Successfully joined the group",
            "group": {"group_id": group.group_id, "group_name": group.group_name},
        }
    )


@groups_bp.delete("/<string:group_id>/members/<string:user_id>")
def remove_member(group_id, user_id):
    db = MongoDatabase().get_db()
    try:
        group_data = db.groups.find_one({"_id": group_id})
        if not group_data:
            return jsonify({"error": "Group not found"}), 404

        group = Group.from_dict(group_data)
        requestor_id = request.json.get("requestor_id")

        if not requestor_id or (
            requestor_id != group.admin_id and requestor_id != user_id
        ):
            return jsonify({"error": "Unauthorized to remove this member"}), 403

        if user_id == group.admin_id:
            return jsonify({"error": "Cannot remove the group admin"}), 400

        if user_id in group.members:
            db.groups.update_one({"_id": group_id}, {"$pull": {"members": user_id}})
            return jsonify({"message": "Member removed successfully"})
        else:
            return jsonify({"error": "User is not a member of this group"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid group ID format"}), 400
