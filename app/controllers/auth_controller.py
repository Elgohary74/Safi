from flask import flash, redirect, request, url_for
from flask_classful import route
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies

from app.controllers.base_controller import IController
from app.models.user import UserLogin, UserRegister
from app.services import AuthService


class AuthController(IController):
    route_base = ""
    route_prefix = "/auth"
    route_base = ""

    def __init__(self):
        self.auth_service = AuthService()

    @route("/register", methods=["POST"])
    def register_user(self):
        """
        Register a new user with the provided details.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The password for the user account.
            phone_number (str, optional): The phone number of the user. Defaults to None.

        Returns:
            User: The registered user object.

        Raises:
            ValueError: If registration fails due to existing email or other issues.
        """
        user_register = UserRegister(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=request.form.get("password"),
            phone_number=request.form.get("phone", None),
        )
        try:
            self.auth_service.register_user(user_register)
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("view.login_view"))
        except Exception as e:
            flash(str(e), "error")
            return redirect(url_for("view.register_view"))

    @route("/login", methods=["POST"])
    def handle_login(self):
        """
        Authenticate a user with the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user account.

        Returns:
            User: The authenticated user object if credentials are valid, else None.
        """
        user_login = UserLogin(
            email=request.form.get("email"),
            password=request.form.get("password"),
        )

        try:
            user, access_token = self.auth_service.authenticate_user(
                user_login.email, user_login.password
            )
            response = redirect(url_for("dashboard.dashboard_index"))
            set_access_cookies(response, access_token)

            flash("Login successful!", "success")
            return response
        except Exception:
            flash("Invalid email or password", "error")
            return redirect(url_for("view.login_view"))

    @route("/logout", methods=["POST"])
    def handle_logout(self):
        """
        Log out the specified user.

        Args:
            user (User): The user object to log out.

        Returns:
            None
        """
        response = redirect(url_for("view.login_view"))
        unset_jwt_cookies(response)
        flash("You have been logged out.", "info")
        return response
