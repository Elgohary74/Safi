from flask import flash, redirect, url_for
from flask_jwt_extended import JWTManager

from app.repositories.user_repo import UserRepository

jwt = JWTManager()


def init_jwt(app):
    jwt.init_app(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        repo = UserRepository()
        return repo.get_by_id(identity)

    @jwt.unauthorized_loader
    def custom_unauthorized_response(_err):
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("view.login_view"))

    @jwt.expired_token_loader
    def custom_expired_token_response(_jwt_header, _jwt_payload):
        flash("Your session has expired. Please log in again.", "warning")
        return redirect(url_for("view.login_view"))

    @jwt.user_lookup_error_loader
    def custom_user_lookup_error(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        flash(f"User account not found: {identity}", "error")
        return redirect(url_for("view.login_view"))

    @jwt.invalid_token_loader
    def custom_invalid_token_loader(_reason):
        flash("Invalid session. Please log in again.", "error")
        return redirect(url_for("view.login_view"))
