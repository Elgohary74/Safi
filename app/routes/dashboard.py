from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.controllers.GroupController import GroupController

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
group_controller = GroupController()


@dashboard_bp.route("/", methods=["GET"])
@login_required
def index():
    result, status_code = group_controller.list_groups(current_user.user_id)

    net_balance = 0
    amount_owed = 0
    amount_owing = 0

    groups = []
    if status_code == 200 and "groups" in result:
        for group in result["groups"]:
            user_balance = 0  # Replace with actual calculation

            groups.append(
                {
                    "id": group["group_id"],
                    "name": group["group_name"],
                    "member_count": 1,  # You might want to calculate this from group["members"] if available
                    "is_active": True,  # Set based on your business logic
                    "user_balance": user_balance,
                }
            )

    return render_template(
        "dashboard.html",
        groups=groups,
        net_balance=net_balance,
        amount_owed=amount_owed,
        amount_owing=amount_owing,
    )


@dashboard_bp.route("/activity")
@login_required
def activity():
    return render_template("activity.html")


@dashboard_bp.route("/settings")
@login_required
def settings():
    return render_template("settings.html")
