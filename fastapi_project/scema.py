from pydantic import BaseModel


class UserModel(BaseModel):
    username:str|None=None
    email:str|None=None
    phonenumber:int
    password:str|None=None


