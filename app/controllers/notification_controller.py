from flask import jsonify, redirect, url_for
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models import User
from app.services.notification import NotificationService


class NotificationController(BaseController):
    route_prefix = "/notifications"

    def __init__(self):
        super().__init__()
        self.notification_service = NotificationService()

    @route("/", methods=["GET"])
    def get_notifications(self):
        user: User = self.current_user
        notifications = self.notification_service.get_user_notifications(user)
        notifications_data = [
            {
                "notification_id": notif.notification_id,
                "message": notif.message,
                "timestamp": notif.timestamp,
                "type": notif.type,
                "is_read": notif.is_read,
            }
            for notif in notifications
        ]
        return jsonify(notifications_data), 200

    @route("/<notif_id>/mark_as_read", methods=["POST"])
    def mark_as_read(self, notif_id):
        self.notification_service.mark_notification_as_read(notif_id)
        return jsonify({"status": "success"}), 200
