from flask import flash, redirect, render_template, request, url_for
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.services import GroupService
from app.services.transaction_service import TransactionService


class TransactionController(BaseController):
    route_prefix = "/transactions"

    def __init__(self):
        super().__init__()
        self.transaction_service = TransactionService()
        self.group_service = GroupService()

    @route("/activity", methods=["GET"])
    def index(self):
        transactions = self.transaction_service.get_user_transactions(
            self.current_user.user_id
        )
        return render_template(
            "activity.html", transactions=transactions, current_user=self.current_user
        )

    @route("/create", methods=["POST"])
    def create_transaction(self):
        pay_to = request.form.get("pay_to")
        amount = request.form.get("amount")
        group_id = request.form.get("group_id")

        try:
            if not group_id:
                raise ValueError(
                    "Group ID is missing. Please settle up from a specific group page."
                )

            self.transaction_service.create_settlement(
                payer_id=self.current_user.user_id,
                receiver_id=pay_to,
                amount=float(amount),
                group_id=group_id,
            )
            flash(f"Settled {amount} with user!", "success")
        except Exception as e:
            flash(str(e), "danger")

        if group_id:
            return redirect(
                url_for("GroupController:get_group_details", group_id=group_id)
            )
        return redirect(url_for("DashboardController:dashboard_index"))
