from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from pydantic import ValidationError

from app.models.user import UserLogin, UserRegister
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = UserRegister(**request.json)
        user = auth_service.register_user(data)

        return jsonify({"message": "User created", "user_id": user.user_id}), 201

    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = UserLogin(**request.json)
        user = auth_service.authenticate_user(data.email, data.password)

        if user:
            login_user(user)
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except ValidationError as e:
        return jsonify(e.errors()), 400


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def get_current_user():
    return jsonify(
        {
            "user_id": current_user.user_id,
            "name": current_user.name,
            "email": current_user.email,
        }
    )
