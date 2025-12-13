from flask_login import logout_user

from app.services import AuthService


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def register_user(
        self, name: str, email: str, password: str, phone_number: str = None
    ):
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
        return self.auth_service.register_user(name, email, password, phone_number)

    def login_user(self, email: str, password: str):
        """
        Authenticate a user with the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user account.

        Returns:
            User: The authenticated user object if credentials are valid, else None.
        """
        return self.auth_service.authenticate_user(email, password)

    def logout_user(self):
        """
        Log out the specified user.

        Args:
            user (User): The user object to log out.

        Returns:
            None
        """
        logout_user()
