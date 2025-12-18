import re
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str
