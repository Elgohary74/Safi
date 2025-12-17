from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User, UserRegister
from app.services.base import BaseService
from app.utils.exceptions import AuthenticationError


class AuthService(BaseService):
    def __init__(self):
        super().__init__()

    def register_user(self, data: UserRegister) -> User:
        if self.user_repo.get_by_email(data.email):
            raise AuthenticationError("User with this email already exists")

        hashed_pw = generate_password_hash(data.password)

        new_user = User(
            name=data.name,
            email=data.email,
            password_hash=hashed_pw,
            phone_number=data.phone_number,
        )

        self.user_repo.add(new_user)
        return new_user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user: User = self.user_repo.get_by_email(email)
        if not user:
            raise AuthenticationError("Invalid email or password")

        if check_password_hash(user.password_hash, password):
            return user

        return None
