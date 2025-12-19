from typing import Optional

from app.models import Notification, User
from app.services.base import BaseService


class NotificationService(BaseService):
    def __init__(self):
        super().__init__()

    def get_user_notifications(self, user: User) -> Optional[list[Notification]]:
        notifications_schemas = self.notification_repo.get_unread_by_user(user.user_id)

        if notifications_schemas is None:
            return None

        return [
            self._convert_schema_to_notification(schema)
            for schema in notifications_schemas
        ]

    def mark_notification_as_read(self, notif_id: str):
        self.notification_repo.mark_as_read(notif_id)
