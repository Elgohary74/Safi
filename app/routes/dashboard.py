from flask import Blueprint, render_template
from flask_jwt_extended import current_user, jwt_required

from app.services import ExpenseService, GroupService, NotificationService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
group_service = GroupService()
expense_service = ExpenseService()
notification_service = NotificationService()


@dashboard_bp.route("/", methods=["GET"], endpoint="dashboard_index")
@jwt_required()
def index():
    raw_groups = group_service.get_user_groups(current_user.user_id)
    groups_dicts = [group.model_dump() for group in raw_groups]

    amount_owed = 0.0
    amount_owing = 0.0
    group_list = []

    for group in groups_dicts:
        group_id = group.get("group_id")

        expenses = expense_service.get_group_expenses(group_id)
        user_balance = 0.0

        for expense in expenses:
            involved_ids = [split.participant.user_id for split in expense.splits]
            if current_user.user_id not in involved_ids:
                continue

            share = -expense.total_amount / len(expense.splits)
            if expense.payer.user_id == current_user.user_id:
                share += expense.total_amount

            user_balance += share

        user_balance = round(user_balance, 2)

        if user_balance > 0:
            amount_owed += user_balance
        elif user_balance < 0:
            amount_owing += abs(user_balance)

        group_list.append(
            {
                "group_id": group_id,
                "name": group.get("group_name"),
                "member_count": (
                    len(group.get("members", [])) if "members" in group else 1
                ),
                "is_active": group.get("is_active", True),
                "user_balance": user_balance,
            }
        )

    net_balance = amount_owed - amount_owing
    group_list.sort(key=lambda x: (not x["is_active"], x["name"]))

    unread_notifications = notification_service.get_unread_notifications(current_user)
    recent_notifications = unread_notifications[:3] if unread_notifications else []

    return render_template(
        "dashboard.html",
        groups=group_list,
        net_balance=round(net_balance, 2),
        amount_owed=round(amount_owed, 2),
        amount_owing=round(amount_owing, 2),
        current_user=current_user,
        recent_notifications=recent_notifications,
    )


@dashboard_bp.route("/activity")
@jwt_required()
def activity():
    notifications = notification_service.get_user_notifications(current_user)
    return render_template(
        "activity.html", current_user=current_user, notifications=notifications
    )


@dashboard_bp.route("/settings")
@jwt_required()
def settings():
    return render_template("settings.html", current_user=current_user)
