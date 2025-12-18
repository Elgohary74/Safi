from flask_classful import FlaskView
from flask_jwt_extended import current_user, jwt_required
from flask_pydantic import validate


class IController(FlaskView):
    decorators = [validate()]


class BaseController(IController):
    route_base = ""
    decorators = IController.decorators + [jwt_required()]

    def __init__(self):
        super().__init__()
        self.current_user = current_user
