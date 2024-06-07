from main import app
from scema import UserModel,LoginModel,UpdateuserModel
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
      return await User.deleteuser(id)


@app.put("/updateuser/")
async def updateuser(userupdate:UpdateuserModel):
     session=session_local()
     user = session.query(User).filter(User.id==userupdate.id).first()
     if user:
          userdata=userupdate.dict(exclude_unset=True)
          _=[ setattr (user,key ,value)  for key ,value in userupdate.dict(exclude_unset=True).items()  ]
          session.commit()
          return HTTPException(status_code=200,detail="User is updated")
     else:
          return HTTPException(status_code=404,detail="User not found",headers={"msg":[]})



