import io
from typing import Optional

from flask import Request, send_file
from flask_jwt_extended import current_user

from app.models.payment_method import PaymentMethod
from app.models.user import UpdateUserRequest, UserPicture
from app.services.base import BaseService
from app.utils.exceptions import ResourceAlreadyExists, ResourceNotFound, UpdateError


class UserService(BaseService):
    def __init__(self):
        super().__init__()

    def update_user_data(self, update_request: UpdateUserRequest) -> bool:
        user = self.get_user(current_user.user_id)
        updated_user = user
        updated_user.name = update_request.new_name
        updated_user.email = update_request.new_email
        updated_user.phone_number = update_request.new_phone_number

        self.user_repo.update(user.user_id, updated_user)

        return True

    def update_user_picture(self, new_user_picture: UserPicture):

        is_updated = self.user_repo.update_picture(
            current_user.user_id, new_user_picture
        )

        if not is_updated:
            raise UpdateError("Failed to update user picture")

    def get_picture_from_request(self, request: Request):
        file = request.files.get("profile_picture")

        if not file:
            raise UpdateError("No file selected")

        content_type = file.content_type
        self.is_picture_format_valid(content_type)
        picture_data = file.read()
        return UserPicture(profile_pic=picture_data, content_type=content_type)

    def is_picture_format_valid(self, content_type: str):
        allowed_types = ["image/jpeg", "image/png"]
        if content_type not in allowed_types:
            raise UpdateError(
                f"Invalid picture format '{content_type}'. The image should be JPEG or PNG."
            )

    def get_user_picture(self, user_id: str) -> Optional[UserPicture]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFound("User not found")

        if not user.user_picture:
            return None

        return self._encode_picture(user.user_picture)

    def _encode_picture(self, user_picture: UserPicture):
        return send_file(
            io.BytesIO(user_picture.profile_pic),
            mimetype=user_picture.content_type,
            as_attachment=False,
            download_name="profile_picture",
        )

    def _payment_methods_equal(
        self,
        first: PaymentMethod,
        second: PaymentMethod,
    ) -> bool:
        return getattr(first, "__dict__", {}) == getattr(second, "__dict__", {})

    def check_if_payment_method_exists(self, payment_method: PaymentMethod) -> None:
        if current_user.payment_methods:
            for existing_method in current_user.payment_methods:
                if self._payment_methods_equal(existing_method, payment_method):
                    raise ResourceAlreadyExists("Payment method already exists")

    def add_new_payment_method(self, payment_method: PaymentMethod) -> bool:
        self.check_if_payment_method_exists(payment_method)
        return self.user_repo.add_payment_method(current_user.user_id, payment_method)
