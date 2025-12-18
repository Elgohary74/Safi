from functools import wraps

from flask import flash, redirect, request, url_for
from flask_login import current_user

from app.services.group import GroupService


def require_group_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        group_id = kwargs.get("group_id")
        if not group_id:
            group_id = request.form.get("group_id") or request.args.get("group_id")

        if not group_id:
            flash("Group ID not found.", "danger")
            return redirect(url_for("dashboard.index"))

        service = GroupService()
        if not service._is_user_first_member_of_group(current_user.user_id, group_id):
            flash("You do not have permission to perform this action.", "danger")
            return redirect(
                url_for("GroupController:get_group_details", group_id=group_id)
            )

        return f(*args, **kwargs)

    return decorated_function
