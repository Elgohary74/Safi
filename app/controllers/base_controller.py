from flask_classful import FlaskView
from flask_login import current_user, login_required
from flask_pydantic import validate


class IController(FlaskView):
    decorators = [validate()]


class BaseController(IController):
    decorators = IController.decorators + [login_required]

    def __init__(self):
        super().__init__()
        self.current_user = current_user
