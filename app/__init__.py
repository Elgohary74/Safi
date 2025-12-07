import os

from flask import Flask

from .config import DevelopmentConfig
from .logging_config import configure_logging
from .routes.auth import auth_bp
from .routes.expenses import expenses_bp
from .routes.groups import groups_bp
from .routes.users import dashboard_bp, users_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(config_class)

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)

    configure_logging(app)
    app.logger.info("Starting up the application...")

    return app
