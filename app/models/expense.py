import uuid
from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field

from app.models.group import Group
from app.models.shared_expense import SharedExpense, SharedExpenseSchema
from app.models.user import User


class ExpenseBase(BaseModel):
    expense_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    total_amount: float
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Expense(ExpenseBase):
    payer: User
    group: Group
    splits: List[SharedExpense] = Field(default_factory=list)


class ExpenseSchema(ExpenseBase):
    payer_id: str
    group_id: str
    splits: List[SharedExpenseSchema] = Field(default_factory=list)
