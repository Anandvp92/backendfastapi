from main import app
from scema import UserModel,LoginModel,UpdateuserModel
from models import User
from database import session_local
from fastapi import HTTPException ,Depends
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import jwt,JWTError

SECRET_KEY ="b360aa7d2fa355afa670ad2480d0b18d931a4f1049413230c6020f5731345f44"
KEY='931158734c8d577bbaa24749957d4ef1'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




@app.post("/createuser/",tags=["Create User"])
async def createuser(user:UserModel):
       return User.create(user)
      
@app.get("/listusers/",tags=["List user"])
async def listuser(db: Session = Depends(User.db)):
        allusers=db.query(User).all()
        if allusers:
            return allusers
        else:
            return HTTPException(status_code=404,detail="No user's")

@app.post("/checkuser/",tags=["Checking User"])
async def checkuser(user:UserModel):
    newuser=User.converttoobject(obj=user)
    return newuser.userexist()

@app.post("/login/",tags=["User Login"])
async def login_user(user:LoginModel):
    return await User.verfiy_password(obj=user)


@app.delete("/deleteuser/{id}",tags=["Delete User"])
async def deleteuser(id:int):
      return  User.deleteuser(id)


@app.put("/updateuser/",tags=["Update User"])
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

@app.get("/checkjwt/")
def checkjwt():
    token = jwt.encode({'key': 'value'}, key= SECRET_KEY, algorithm=ALGORITHM)
    updatetoken=jwt.decode(token,key=SECRET_KEY,algorithms=ALGORITHM)
    return updatetoken
    


