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

    net_balance = 0.0
    amount_owed = 0.0
    amount_owing = 0.0
    group_list = []

    for group in groups_dicts:
        user_balance = 0.0
        debts = group.get("debts", [])
        for debt in debts:
            # debt: {from_user, to_user, amount, currency}
            if debt["to_user"] == current_user.user_id:
                user_balance += debt["amount"]
                amount_owed += debt["amount"]
            elif debt["from_user"] == current_user.user_id:
                user_balance -= debt["amount"]
                amount_owing += debt["amount"]
        group_list.append(
            {
                "id": group.get("group_id"),
                "name": group.get("group_name"),
                "member_count": (
                    len(group.get("members", [])) if "members" in group else 1
                ),
                "is_active": True,
                "user_balance": user_balance,
            }
        )

    net_balance = amount_owed - amount_owing

    return render_template(
        "dashboard.html",
        groups=group_list,
        net_balance=round(net_balance, 2),
        amount_owed=round(amount_owed, 2),
        amount_owing=round(amount_owing, 2),
        current_user=current_user,
    )


@dashboard_bp.route("/activity")
@jwt_required()
def activity():
    return render_template("activity.html", current_user=current_user)


@dashboard_bp.route("/settings")
@jwt_required()
def settings():
    return render_template("settings.html", current_user=current_user)
