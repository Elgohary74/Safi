from typing import List, Optional

from app.models.notification import Notification
from app.repositories.base import IRepository


class NotificationRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["notifications"]

    def add(self, notification: Notification) -> str:
        self.logger.info(f"sending notification to user {notification.user_id}")
        self.collection.insert_one(notification.to_dict())
        return notification.notification_id

    def get_by_id(self, notif_id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": notif_id})

    def get_unread_by_user(self, user_id: str) -> List[dict]:
        return list(self.collection.find({"user_id": user_id, "is_read": False}))

    def mark_as_read(self, notif_id: str):
        self.logger.debug(f"marking notification {notif_id} as read")
        self.collection.update_one({"_id": notif_id}, {"$set": {"is_read": True}})

    def update(self, id: str, data: dict):
        self.collection.update_one({"_id": id}, {"$set": data})

    def delete(self, id: str):
        self.collection.delete_one({"_id": id})
