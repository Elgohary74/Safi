from flask import Blueprint, jsonify, request

from app.models.user import User
from app.repositories.user_repo import UserRepository

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.post("/")
def add_user():
    data = request.get_json()

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password_hash=data.get("password_hash"),
        phone_number=data.get("phone_number"),
    )

    user_repository = UserRepository()
    user_id = user_repository.add(new_user)

    return jsonify({"id": str(user_id)}), 201
