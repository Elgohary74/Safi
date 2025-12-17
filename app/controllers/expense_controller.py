from flask import flash, redirect, request, url_for
from flask_classful import route

from app.controllers.base_controller import BaseController
from app.models.expense import ExpenseCreationRequest
from app.services import ExpenseService


class ExpenseController(BaseController):
    route_prefix = "/expenses"

    def __init__(self):
        super().__init__()
        self.expense_service = ExpenseService()

    @route("/create", methods=["POST"])
    def create_expense(self):
        expense_request = ExpenseCreationRequest(**request.form.to_dict())
        new_expense = self.expense_service.create_new_expense(expense_request)
        self.expense_service.save_new_expense(new_expense)

        flash("Expense added successfully!", "success")

        return redirect(url_for("GroupController:list_groups"))
