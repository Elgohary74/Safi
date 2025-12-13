from typing import Literal

from pydantic import BaseModel, Field

from app.models.user import User


class SharedExpenseBase(BaseModel):
    amount: float
    status: Literal["unpaid", "paid", "pending"] = Field(default="unpaid")


class SharedExpense(SharedExpenseBase):
    participant: User


class SharedExpenseSchema(SharedExpenseBase):
    participant_id: str
