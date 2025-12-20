from datetime import datetime, timezone

from app.events.signals import expense_created
from app.models import Expense
from app.models.expense import ExpenseCreationRequest, ExpenseUpdateRequest
from app.services.base import BaseService
from app.utils.exceptions import CreationError, ResourceNotFound


class ExpenseService(BaseService):
    def __init__(self):
        super().__init__()

    def create_new_expense(self, request: ExpenseCreationRequest) -> Expense:
        group = self.get_group(request.group_id)
        if not group.is_active:
            raise CreationError(message="Cannot add expense to an inactive group")

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
        expense_created.send(self, expense=expense)
        return expense_id

    def update_expense(self, expense_id: str, update_expense_request: ExpenseUpdateRequest) -> None:
        expense_schema = self.expense_repo.get_by_id(expense_id)
        if not expense_schema:
             raise ResourceNotFound(message="Expense not found")
            
        expense_schema.total_amount = update_expense_request.total_amount
        expense_schema.description = update_expense_request.description
        expense_schema.payer_id = update_expense_request.payer_id
        
        self.expense_repo.update(expense_id, expense_schema)
        

    def get_group_expenses(self, group_id: str) -> list[Expense]:
        expenses_schemas = self.expense_repo.get_all_by_group(group_id)
        return [
            self._convert_schema_to_expense(expense_schema)
            for expense_schema in expenses_schemas
        ]
