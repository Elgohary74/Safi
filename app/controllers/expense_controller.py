from datetime import datetime

from flask import flash, redirect, request
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models.debt import Debt
from app.models.expense import Expense, ExpenseCreationRequest, ExpenseUpdateRequest, SharedExpense
from app.services import ExpenseService, GroupService


class ExpenseController(BaseController):
    route_prefix = "/expenses"

    def __init__(self):
        super().__init__()
        self.expense_service = ExpenseService()
        self.group_service = GroupService()

    @route("/create", methods=["POST"])
    def create_expense(self):
        expense_request = ExpenseCreationRequest(**request.form.to_dict())

        participant_ids = request.form.getlist("split_with")
        group = self.expense_service.get_group(expense_request.group_id)
        if not group.is_active:
            flash("Cannot add expense to an inactive group", "error")
            return redirect(request.referrer)

        payer = self.expense_service.get_user(expense_request.payer_id)

        num_participants = len(participant_ids)
        if num_participants < 2:
            flash("Please select at least two participants.", "error")
            return redirect(request.referrer)
        share_amount = round(expense_request.total_amount / num_participants, 2)

        splits = []
        for user_id in participant_ids:
            user = self.expense_service.get_user(user_id)
            if user is None:
                flash(f"User not found: {user_id}", "error")
                continue
            splits.append(
                {"participant": user, "amount": share_amount, "status": "unpaid"}
            )

        new_expense = Expense(
            description=expense_request.description,
            total_amount=expense_request.total_amount,
            date=datetime.now(),
            payer=payer,
            group=group,
            splits=[SharedExpense(**split) for split in splits],
        )
        self.expense_service.save_new_expense(new_expense)

        debts = group.debts if hasattr(group, "debts") else []
        for user_id in participant_ids:
            if user_id != payer.user_id:
                debts.append(
                    Debt(from_user=user_id, to_user=payer.user_id, amount=share_amount)
                )
        group.debts = debts
        self.group_service.group_repo.update(
            group.group_id, self.group_service._convert_group_to_schema(group)
        )

        flash("Expense added and split successfully!", "success")
        return redirect(request.referrer)

    @route("/<expense_id>/update", methods=["POST"])
    def update_expense(self, expense_id):
        self.expense_service.update_expense(expense_id, ExpenseUpdateRequest(**request.form.to_dict()))
        flash("Expense updated successfully!", "success")
        return redirect(request.referrer)
