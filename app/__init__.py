import os

from flask import Flask
from flask_login import LoginManager

from app.controllers import AuthController, GroupController, ExpenseController
from app.repositories.user_repo import UserRepository
from app.utils import register_error_handlers

from .config import DevelopmentConfig
from .logging_config import configure_logging
from .routes.dashboard import dashboard_bp
from .routes.view import view_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(config_class)

    configure_logging(app)
    register_error_handlers(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    # This function is used by Flask-Login to reload the user object
    # from the user ID stored in the session
    @login_manager.user_loader
    def load_user(user_id):
        repo = UserRepository()
        return repo.get_by_id(user_id)

    # register blueprints
    AuthController.register(app)
    GroupController.register(app)
    ExpenseController.register(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(view_bp)

    app.logger.info("Starting up the application...")

    return app
