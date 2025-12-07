from flask import Blueprint, render_template


expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.route("/create")
def create():
    pass
