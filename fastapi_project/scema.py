from pydantic import BaseModel,ValidationError,validator,EmailStr
from typing import Optional


class UserModel(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    phonenumber: int
    password: Optional[str] = None

    @validator("email")
    def email_validator(cls, value):
        if not value.endswith("@example.com"):
            raise ValueError("Email is not a valid one")
        return value

    @validator("phonenumber")
    def phonenumber_validator(cls, value):
        str_value = str(value)
        if len(str_value) != 10 or not str_value.isdigit():
            raise ValueError("Phone number must be a 10-digit number")
        return value