from flask import Blueprint, render_template, g
from pymongo import MongoClient
from bson.objectid import ObjectId

users_bp = Blueprint("users", __name__, url_prefix="/users")
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@users_bp.get("/")
def list_users():
    return {"message": "list all users"}


@dashboard_bp.route("/")
def index():
    # Get the current user ID (adjust based on your authentication system)
    user_id = g.current_user["_id"] if hasattr(g, "current_user") else None

    # Initialize empty variables for the dashboard stats
    net_balance = 0
    amount_owed = 0
    amount_owing = 0

    # Fetch groups from MongoDB where the current user is a member
    groups = []
    if user_id:
        # Connect to MongoDB (adjust based on your app's configuration)
        client = MongoClient("mongodb://localhost:27017/")
        db = client.your_database_name

        # Find all groups where the user is a member
        groups_cursor = db.groups.find({"members": user_id})

        for group in groups_cursor:
            # Calculate the user's balance for this group
            # This is just an example, you'll need to adapt based on your data model
            user_balance = 0
            if "balances" in group and user_id in group["balances"]:
                user_balance = group["balances"][user_id]

            # Format the group data for the template
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
