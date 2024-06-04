from main import app
from scema import UserModel
from models import User
from database import session_local
from fastapi import HTTPException 


@app.post("/createuser/")
def createuser(user:UserModel):
    User.create(userinstance=user)
    return HTTPException(status_code=200 ,detail="User created sucessfully")