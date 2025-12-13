from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from pydantic import ValidationError

from app.controllers import AuthController
from app.models.user import UserLogin, UserRegister

auth_bp = Blueprint("auth", __name__)
auth_controller = AuthController()


@auth_bp.route("/register", methods=["POST"])
def register():
    is_json_request = request.is_json
    try:
        if is_json_request:
            data = UserRegister(**request.json)
        else:
            data = UserRegister(
                name=request.form.get("name"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                phone_number=request.form.get("phone", None),
            )

        user = auth_controller.register_user(data)

        if is_json_request:
            return jsonify({"message": "User created", "user_id": user.user_id}), 201
        else:
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))

    except ValidationError as e:
        if is_json_request:
            return jsonify(e.errors()), 400
        else:
            flash(f"Validation error: {str(e)}", "error")
            return render_template("auth_register.html")

    except ValueError as e:
        if is_json_request:
            return jsonify({"error": str(e)}), 409
        else:
            flash(str(e), "error")
            return render_template("auth_register.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    is_json_request = request.is_json

    try:
        if is_json_request:
            data = UserLogin(**request.json)
            email = data.email
            password = data.password
        else:
            email = request.form.get("email")
            password = request.form.get("password")

        user = auth_controller.login_user(email, password)

        if user:
            login_user(user)

            if is_json_request:
                return jsonify({"message": "Login successful"}), 200
            else:
                flash("Login successful!", "success")
                return redirect(url_for("dashboard.index"))  # Redirect to dashboard
        else:
            if is_json_request:
                return jsonify({"error": "Invalid credentials"}), 401
            else:
                flash("Invalid email or password. Please try again.", "error")
                return render_template("auth_login.html")

    except ValidationError as e:
        if is_json_request:
            return jsonify(e.errors()), 400
        else:
            flash(f"Validation error: {str(e)}", "error")
            return render_template("auth_login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    auth_controller.logout_user()
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
