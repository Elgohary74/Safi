from flask import Blueprint, g, render_template, jsonify, request

from app.models.user import User
from app.repositories.user_repo import UserRepository

from pymongo import MongoClient

users_bp = Blueprint("users", __name__, url_prefix="/users")
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@users_bp.post("/")
def add_user():
    data = request.get_json()

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password_hash=data.get("password_hash"),
        phone_number=data.get("phone_number"),
    )

    user_repository = UserRepository()
    user_id = user_repository.add(new_user)

    return jsonify({"id": str(user_id)}), 201


@dashboard_bp.route("/")
def index():
    user_id = g.current_user["_id"] if hasattr(g, "current_user") else None

    net_balance = 0
    amount_owed = 0
    amount_owing = 0

    groups = []
    if user_id:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.your_database_name

        groups_cursor = db.groups.find({"members": user_id})

        for group in groups_cursor:
            user_balance = 0
            if "balances" in group and user_id in group["balances"]:
                user_balance = group["balances"][user_id]

            groups.append(
                {
                    "id": str(group["_id"]),
                    "name": group["name"],
                    "member_count": len(group.get("members", [])),
                    "is_active": group.get("is_active", True),
                    "user_balance": user_balance,
                }
            )

            # Update dashboard stats
            if user_balance > 0:
                amount_owed += user_balance
            else:
                amount_owing += abs(user_balance)

        net_balance = amount_owed - amount_owing

    # Render the dashboard template with the fetched groups and calculated stats
    return render_template(
        "dashboard.html",
        groups=groups,
        net_balance=net_balance,
        amount_owed=amount_owed,
        amount_owing=amount_owing,
    )


@dashboard_bp.route("/activity")
def activity():
    return render_template("activity.html")


@dashboard_bp.route("/settings")
def settings():
    return render_template("settings.html")
