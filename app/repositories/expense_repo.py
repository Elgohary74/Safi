from typing import List, Optional

from app.models.expense import Expense

from .base import IRepository


class ExpenseRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["expenses"]

    def add(self, expense: Expense) -> str:
        self.logger.info(
            f"recording expense: {expense.description} ({expense.total_amount})"
        )
        self.collection.insert_one(expense.to_dict())
        return expense.expense_id

    def get_by_id(self, expense_id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": expense_id})

    def get_all_by_group(self, group_id: str) -> List[dict]:
        self.logger.debug(f"fetching all expenses for group {group_id}")
        cursor = self.collection.find({"group_id": group_id})
        return list(cursor)

    def update(self, expense_id: str, data: dict):
        self.collection.update_one({"_id": expense_id}, {"$set": data})

    def delete(self, expense_id: str):
        self.collection.delete_one({"_id": expense_id})
