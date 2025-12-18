from app.controllers.base_controller import BaseController
from app.services import UserService
from flask_classful import route
from flask import request, flash, redirect
from app.models.user import UpdateUserRequest


class UserController(BaseController):
    route_prefix = "/user"

    def __init__(self):
        super().__init__()
        self.user_service = UserService()

    @route("/update_profile", methods=["POST"])
    def update_profile(self):
        update_profile_request = UpdateUserRequest(**request.form.to_dict())

        result = self.user_service.update_user_data(update_profile_request)

        if result:
            flash("Profile updated successfully!", "success")
        else:
            flash("Please Enter a Valid Email or Name", "error")

        return redirect(request.referrer)
