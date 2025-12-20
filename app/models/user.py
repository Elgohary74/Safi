import re
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.payment_method import PaymentMethod
from app.utils.exceptions import InvalidPasswordFormat


class UserPicture(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    profile_pic: Optional[bytes] = None
    content_type: Optional[str] = None


class IUser(BaseModel):
    name: str
    email: EmailStr


class UserBase(IUser):
    phone_number: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    password_hash: str
    user_picture: Optional[UserPicture] = None
    payment_methods: list[PaymentMethod] = Field(default_factory=list)


class UserRegister(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise InvalidPasswordFormat("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise InvalidPasswordFormat(
                "Password must contain at least one uppercase letter"
            )
        if not re.search(r"[a-z]", v):
            raise InvalidPasswordFormat(
                "Password must contain at least one lowercase letter"
            )
        if not re.search(r"\d", v):
            raise InvalidPasswordFormat("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise InvalidPasswordFormat(
                "Password must contain at least one special character"
            )
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UpdateUserRequest(BaseModel):
    new_name: str
    new_email: EmailStr
    new_phone_number: Optional[str]
