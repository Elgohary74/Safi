from flask import jsonify

from app.utils.exceptions import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        return jsonify({"error": e.message, "details": e.payload}), e.status_code
