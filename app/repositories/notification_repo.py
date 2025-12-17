from typing import List, Optional

from app.models import NotificationSchema
from app.repositories.base import IRepository


class NotificationRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["notifications"]

    def add(self, notification: NotificationSchema) -> str:
        self.logger.info(f"sending notification to user {notification.user_id}")
        self.collection.insert_one(notification.model_dump())
        return notification.notification_id

    def get_by_id(self, notif_id: str) -> Optional[NotificationSchema]:
        self.logger.debug(f"fetching notification id: {notif_id}")
        data = self.collection.find_one({"_id": notif_id})
        return NotificationSchema.model_validate(data) if data else None

    def get_unread_by_user(self, user_id: str) -> List[NotificationSchema]:
        self.logger.debug(f"fetching unread notifications for user {user_id}")
        data_list = list(self.collection.find({"user_id": user_id, "is_read": False}))
        return [NotificationSchema.model_validate(data) for data in data_list]

    def mark_as_read(self, notif_id: str):
        self.logger.debug(f"marking notification {notif_id} as read")
        self.collection.update_one({"_id": notif_id}, {"$set": {"is_read": True}})

    def update(self, id: str, data: NotificationSchema):
        self.logger.info(f"updating notification id: {id}")
        self.collection.update_one({"_id": id}, {"$set": data.model_dump()})

    def delete(self, id: str):
        self.logger.info(f"deleting notification id: {id}")
        self.collection.delete_one({"_id": id})
