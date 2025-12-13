from flask import Blueprint, render_template

view_bp = Blueprint("view", __name__)


@view_bp.route("/auth/register", methods=["GET"])
def register_view():
    return render_template("auth_register.html")


@view_bp.route("/auth/login", methods=["GET"])
def login_view():
    return render_template("auth_login.html")
