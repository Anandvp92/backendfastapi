from pydantic import BaseModel,ValidationError,validator,EmailStr


class UserModel(BaseModel):
    username:str|None=None
    email:EmailStr
    phonenumber:int 
    password:str|None=None

    @classmethod
    @validator("email")
    def email_validator(cls,instance):
        if not instance and not instance.endswith("@example.com"):
            raise ValueError("Email is not a valid one")
        return instance

    @validator("phonenumber")
    def phonenumber_validator(cls,instance):
        str_value=str(instance)
        if len(str_value)!=10:
            raise ValueError("Phone number is not valid")
        return instance