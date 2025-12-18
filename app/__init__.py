from flask import Flask

from app.controllers import AuthController, GroupController
from app.utils import register_error_handlers
from app.utils.jwt_manager import init_jwt

from .config import DevelopmentConfig
from .logging_config import configure_logging
from .routes.dashboard import dashboard_bp
from .routes.expenses import expenses_bp
from .routes.view import view_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    configure_logging(app)
    register_error_handlers(app)

    init_jwt(app)

    AuthController.register(app)
    GroupController.register(app)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(view_bp)

    app.logger.info("Starting up the application...")

    return app
