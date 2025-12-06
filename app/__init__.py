from flask import Flask

from app.config import DevelopmentConfig
from app.logging_config import configure_logging
from .routes import auth_bp, groups_bp, users_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(auth_bp)

    configure_logging(app)
    app.logger.info("Starting up the application...")

    return app
