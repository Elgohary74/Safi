from flask import Blueprint, render_template
from flask_jwt_extended import current_user, jwt_required

view_bp = Blueprint("view", __name__)


@view_bp.route("/auth/register", methods=["GET"])
@jwt_required(optional=True)
def register_view():
    return render_template("auth_register.html", current_user=current_user)


@view_bp.route("/auth/login", methods=["GET"])
@jwt_required(optional=True)
def login_view():
    return render_template("auth_login.html", current_user=current_user)
