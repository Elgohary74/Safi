from flask import render_template
from flask_jwt_extended import current_user

from app.utils.exceptions import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        from flask_jwt_extended import verify_jwt_in_request

        try:
            verify_jwt_in_request(optional=True)
            user = current_user
        except Exception:
            user = None

        return (
            render_template(
                "error.html",
                error_code=e.status_code,
                error_message=e.message,
                current_user=user,
            ),
            e.status_code,
        )
