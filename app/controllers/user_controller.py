from flask import flash, redirect, request
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models.user import UpdateUserRequest
from app.services import UserService


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

    @route("/update_picture", methods=["POST"])
    def update_picture(self):
        picture = self.user_service.get_picture_from_request(request)
        self.user_service.update_user_picture(picture)
        flash("Profile picture updated successfully!", "success")

        return redirect(request.referrer)

    @route("/picture/<user_id>", methods=["GET"])
    def get_picture(self, user_id: str):
        return self.user_service.get_user_picture(user_id)
