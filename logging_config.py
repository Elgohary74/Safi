import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from flask import Flask


def configure_logging(app: Flask):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_level = logging.DEBUG if app.debug else logging.INFO
    app.logger.setLevel(log_level)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/safi_app.log", maxBytes=10240000, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    del app.logger.handlers[:]
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    app.logger.info(" application Logging System Initialized")
