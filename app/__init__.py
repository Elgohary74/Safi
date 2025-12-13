import os

from flask import Flask
from flask_login import LoginManager

from app.repositories.user_repo import UserRepository

from .config import DevelopmentConfig
from .logging_config import configure_logging
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.expenses import expenses_bp
from .routes.groups import groups_bp
from .routes.users import users_bp
from .routes.view import view_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(config_class)

    login_manager = LoginManager()
    login_manager.init_app(app)

    # This function is used by Flask-Login to reload the user object
    # from the user ID stored in the session
    @login_manager.user_loader
    def load_user(user_id):
        repo = UserRepository()
        return repo.get_by_id(user_id)

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(view_bp)

    configure_logging(app)
    app.logger.info("Starting up the application...")

    return app
