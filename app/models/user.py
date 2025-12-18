import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    email: str
    password_hash: str
    phone_number: Optional[str] = None


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
