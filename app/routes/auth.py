from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login")
def login():
    return render_template("auth_login.html")


@auth_bp.route("/register")
def register():
    return render_template("auth_register.html")


@auth_bp.route("/logout")
def logout():
    pass
