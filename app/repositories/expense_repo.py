from typing import List, Optional

from app.models import ExpenseSchema

from .base import IRepository


class ExpenseRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["expenses"]

    def add(self, expense: ExpenseSchema) -> str:
        self.logger.info(
            f"recording expense: {expense.description} ({expense.total_amount})"
        )
        self.collection.insert_one(expense.model_dump())
        return expense.expense_id

    def get_by_id(self, expense_id: str) -> Optional[ExpenseSchema]:
        self.logger.debug(f"fetching expense id: {expense_id}")
        data = self.collection.find_one({"expense_id": expense_id})
        return ExpenseSchema.model_validate(data) if data else None

    def get_all_by_group(self, group_id: str) -> List[ExpenseSchema]:
        self.logger.debug(f"fetching all expenses for group {group_id}")
        cursor = self.collection.find({"group_id": group_id})
        return [ExpenseSchema.model_validate(doc) for doc in cursor]

    def update(self, expense_id: str, data: ExpenseSchema):
        self.logger.info(f"updating expense id: {expense_id}")
        self.collection.update_one({"expense_id": expense_id}, {"$set": data.model_dump()})

    def delete(self, expense_id: str):
        self.logger.info(f"deleting expense id: {expense_id}")
        self.collection.delete_one({"expense_id": expense_id})
