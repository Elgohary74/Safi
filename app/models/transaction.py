import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

from app.models.group import Group
from app.models.user import User


class TransactionBase(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    amount: float
    status: Literal["pending", "completed", "failed"] = Field(default="pending")
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Transaction(TransactionBase):
    payer: User
    receiver: User
    group: Group


class TransactionSchema(TransactionBase):
    payer_id: str
    receiver_id: str
    group_id: str
