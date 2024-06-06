from pydantic import BaseModel,ValidationError,validator,EmailStr,validate_email
from typing import Optional
import re

class UserModel(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    phonenumber: Optional[int] =None
    password: Optional[str] = None

    @validator("email")
    def email_validator(cls, value):
        if not validate_email(value):
            raise ValueError("Email is not a valid one")
        return value

    @validator("phonenumber")
    def phonenumber_validator(cls, value):
        str_value = str(value)        
        if not re.compile(r'^\d{10}$').match(str_value):
            raise ValueError("Phone number must be a 10-digit number")
        return value


class LoginModel(BaseModel):
    email:EmailStr|None=None
    password:str |None=None


class Token(BaseModel):
    acess_token:str
    token_type:str