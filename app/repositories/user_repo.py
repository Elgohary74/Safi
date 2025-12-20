from typing import Optional

from app.models.user import User, UserPicture

from .base import IRepository


class UserRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["users"]

    def add(self, user: User) -> str:
        self.logger.info(f"adding new user: {user.email}")
        self.collection.insert_one(user.model_dump(by_alias=True))
        return user.user_id

    def get_by_id(self, user_id: str) -> Optional[User]:
        self.logger.debug(f"fetching user id: {user_id}")
        data = self.collection.find_one({"_id": user_id})
        return User(**data) if data else None

    def get_by_email(self, email: str) -> Optional[User]:
        self.logger.debug(f" get user by email: {email}")
        data = self.collection.find_one({"email": email})
        return User(**data) if data else None

    def update(self, user_id: str, data: User):
        self.logger.info(f"updating user {user_id}")
        self.collection.update_one(
            {"_id": user_id}, {"$set": data.model_dump(by_alias=True)}
        )

    def update_picture(self, user_id: str, user_picture: UserPicture):
        self.logger.info(f"updating user picture for user {user_id}")
        self.collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "user_picture": {
                        "profile_pic": user_picture.profile_pic,
                        "content_type": user_picture.content_type,
                    }
                }
            },
        )

        return True

    def delete(self, user_id: str):
        self.logger.warning(f"deleting user {user_id}")
        self.collection.delete_one({"_id": user_id})
