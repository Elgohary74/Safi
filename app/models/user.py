import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    email: str
    password_hash: str
    phone_number: Optional[str] = None
