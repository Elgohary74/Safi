from flask import Blueprint, render_template
from flask_jwt_extended import current_user, jwt_required

from app.services import GroupService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
group_service = GroupService()


@dashboard_bp.route("/", methods=["GET"], endpoint="dashboard_index")
@jwt_required()
def index():
    # Fetch groups as Pydantic models
    raw_groups = group_service.get_user_groups(current_user.user_id)

    # Convert to list of dicts for processing
    groups_dicts = [group.model_dump() for group in raw_groups]

    net_balance = 0
    amount_owed = 0
    amount_owing = 0

    group_list = []

    # Process the groups to match the structure expected by dashboard.html
    for group in groups_dicts:
        user_balance = 0  # Logic to calculate balance goes here

        # Ensure keys here match what is used in dashboard.html (e.g., group.id, group.name)
        group_list.append(
            {
                "id": group.get("group_id"),  # Map DB 'group_id' to Template 'id'
                "name": group.get(
                    "group_name"
                ),  # Map DB 'group_name' to Template 'name'
                "member_count": (
                    len(group.get("members", [])) if "members" in group else 1
                ),
                "is_active": True,
                "user_balance": user_balance,
            }
        )

    return render_template(
        "dashboard.html",
        groups=group_list,  # FIX: Pass the processed 'group_list', not the raw data
        net_balance=net_balance,
        amount_owed=amount_owed,
        amount_owing=amount_owing,
    )


@dashboard_bp.route("/activity")
@jwt_required()
def activity():
    return render_template("activity.html")


@dashboard_bp.route("/settings")
@jwt_required()
def settings():
    return render_template("settings.html")
