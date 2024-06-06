from main import app
from scema import UserModel,LoginModel
from models import User
from database import session_local
from fastapi import HTTPException ,Depends
from sqlalchemy.orm import Session
from fastapi import Depends


@app.post("/createuser/")
async def createuser(user:UserModel):
       return User.create(user)
      
@app.get("/listusers/")
async def listuser(db: Session = Depends(User.db)):
        allusers=db.query(User).all()
        if allusers:
            return allusers
        else:
            return HTTPException(status_code=404,detail="No user's")

@app.post("/checkuser/")
async def checkuser(user:UserModel):
    newuser=User.converttoobject(obj=user)
    return newuser.userexist()

@app.post("/login/")
async def login_user(user:LoginModel):
    return await User.verfiy_password(obj=user)


@app.delete("/deleteuser/{id}")
async def deleteuser(id:int):
        db=next(User.db())
        user=db.query(User).filter(User.id==id).first()
        if user:
            db.delete(user)
            db.commit()
            return HTTPException(status_code=200,detail={"msg":"User deleted"})
        else:
            return HTTPException(status_code=204,detail={"msg":"User not found"})


