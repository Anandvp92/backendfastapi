from main import app
from scema import UserModel
from models import User
from database import session_local
from fastapi import HTTPException ,Depends
from sqlalchemy.orm import Session


@app.post("/createuser/")
async def createuser(user:UserModel):
        User.create(userinstance=user)
        return HTTPException(status_code=200 , detail="User created")
        
@app.get("/listusers/")
async def listuser(user:UserModel,db: Session = Depends(User.db)):
    if User.verify(user):
        allusers=db.query(User).all()
        return allusers

@app.post("/checkuser/")
async def checkuser(user:UserModel):
    newuser=User.converttoobject(obj=user)
    return newuser.userexist()
