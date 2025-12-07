from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User, UserRegister
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, data: UserRegister) -> User:
        if self.user_repo.get_by_email(data.email):
            raise ValueError("User with this email already exists")

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
        user = self.user_repo.get_by_email(email)
        if not user:
            return None

        if check_password_hash(user.password_hash, password):
            return user

        return None
