from flask import flash, redirect, request
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models.payment_method import PaymentMethod
from app.models.user import UpdateUserRequest
from app.services import UserService
from app.utils.payment_factory import PaymentFactory


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

    @route("/add_payment_method", methods=["POST"])
    def add_payment_method(self):
        data = request.get_json(silent=True) or request.form.to_dict()
        payment_method: PaymentMethod = PaymentFactory.create_payment_method(data)
        self.user_service.add_new_payment_method(payment_method)
        flash("Payment method added successfully!", "success")

        return redirect(request.referrer)

    @route("/remove_payment_method", methods=["POST"])
    def remove_payment_method(self):
        data = request.get_json(silent=True) or request.form.to_dict()
        try:
            payment_method: PaymentMethod = PaymentFactory.create_payment_method(data)
            if self.user_service.remove_payment_method(payment_method):
                flash("Payment method removed successfully!", "success")
            else:
                flash("Payment method not found.", "error")
        except Exception as e:
            flash(f"Error removing payment method: {str(e)}", "error")
        return redirect(request.referrer)
