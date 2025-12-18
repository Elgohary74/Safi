import os

from flask import Flask

from app.controllers import __all__ as all_controllers
from app.utils import register_error_handlers
from app.utils.jwt_manager import init_jwt

from .config import DevelopmentConfig
from .logging_config import configure_logging
from .routes.dashboard import dashboard_bp
from .routes.view import view_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = os.urandom(24)
    configure_logging(app)
    register_error_handlers(app)

    init_jwt(app)

    for i in range(len(all_controllers)):
        all_controllers[i].register(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(view_bp)

    app.logger.info("Starting up the application...")

    return app
