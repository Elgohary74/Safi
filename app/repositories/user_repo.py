from typing import Optional

from app.models.user import User

from .base import IRepository


class UserRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["users"]

    def add(self, user: User) -> str:
        self.logger.info(f"adding new user: {user.email}")
        self.collection.insert_one(user.to_dict())
        return user.user_id

    def get_by_id(self, user_id: str) -> Optional[dict]:
        self.logger.debug(f"fetching user id: {user_id}")
        return self.collection.find_one({"_id": user_id})

    def get_by_email(self, email: str) -> Optional[dict]:
        self.logger.debug(f" get user by email: {email}")
        return self.collection.find_one({"email": email})

    def update(self, user_id: str, data: dict):
        self.logger.info(f"updating user {user_id}")
        self.collection.update_one({"_id": user_id}, {"$set": data})

    def delete(self, user_id: str):
        self.logger.warning(f"deleting user {user_id}")
        self.collection.delete_one({"_id": user_id})
