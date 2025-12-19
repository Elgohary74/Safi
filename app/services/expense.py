from datetime import datetime, timezone

from flask_login import current_user

from app.models import Expense
from app.models.expense import ExpenseCreationRequest
from app.services.base import BaseService
from app.utils.exceptions import CreationError


class ExpenseService(BaseService):
    def __init__(self):
        super().__init__()

    def create_new_expense(self, request: ExpenseCreationRequest) -> Expense:
        group = self.get_group(request.group_id)
        payer = self.get_user(request.payer_id)

        new_expense = Expense(
            description=request.description,
            total_amount=request.total_amount,
            date=datetime.now(timezone.utc),
            payer=payer,
            group=group,
        )
        return new_expense

    def save_new_expense(self, expense: Expense) -> str:
        expense_schema = self._convert_expense_to_schema(expense)
        expense_id = self.expense_repo.add(expense_schema)
        if not expense_id:
            raise CreationError(message="Failed to create expense")
        return expense_id

    def get_group_expenses(self, group_id: str) -> list[Expense]:
        expenses_schemas = self.expense_repo.get_all_by_group(group_id)
        return [
            self._convert_schema_to_expense(expense_schema)
            for expense_schema in expenses_schemas
        ]
