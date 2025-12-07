from typing import Optional

from app.models.user import User

from .base import IRepository


class UserRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["users"]

    def add(self, user: User) -> str:
        self.collection.insert_one(user.model_dump(by_alias=True))
        return user.user_id

    def get_by_id(self, user_id: str) -> Optional[User]:
        data = self.collection.find_one({"_id": user_id})
        return User(**data) if data else None

    def get_by_email(self, email: str) -> Optional[User]:
        data = self.collection.find_one({"email": email})
        return User(**data) if data else None

    def update(self, user_id: str, data: dict):
        self.collection.update_one({"_id": user_id}, {"$set": data})

    def delete(self, user_id: str):
        self.collection.delete_one({"_id": user_id})
