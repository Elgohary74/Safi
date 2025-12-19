from flask_jwt_extended import current_user

from app.models.user import UpdateUserRequest
from app.services.base import BaseService


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
