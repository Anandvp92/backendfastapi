from database import Base,engine
from sqlalchemy import Column,Integer,String,Boolean,DateTime,and_
from database import session_local
from fastapi import HTTPException,Depends
from passlib.context import CryptContext
from jose import jwt , JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated



SECRET_KEY ="b360aa7d2fa355afa670ad2480d0b18d931a4f1049413230c6020f5731345f44"
KEY='931158734c8d577bbaa24749957d4ef1'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# router = APIRouter(
#     prefix="/auth",
#     tags=['auth']
# )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth2_bearer= OAuth2PasswordBearer(tokenUrl='auth/token')




class User(Base):
    __tablename__ = "User"
    id = Column("User_ID",Integer,primary_key=True,index=True)
    username = Column("Username",String(225),unique=True,nullable=False)
    email = Column("Email",String(225),unique=True,nullable=False)
    phonenumber = Column("Phonenumber",Integer,unique=True,nullable=False)
    password = Column("Password",String(50))
    is_admin = Column("Is_admin",Boolean,default=False)
    is_staff = Column("Is_staff",Boolean,default=True)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.username=self.username.strip().upper()
        self.email= self.email.strip().lower()
        self.password=self.hashpassword()

    @staticmethod
    def db():
        session = session_local()
        try:
            yield session
        finally:
            session.close()

    def hashpassword(self):
        return pwd_context.hash(self.password)



    @classmethod
    def verfiy_password(cls,obj):
        try:
            if obj:
                session=next(cls.db())
                user=session.query(User).filter( and_(User.email==obj.email.strip())).first()
                if user:
                    if pwd_context.verify(obj.password,user.password):
                        return HTTPException(status_code=200,detail="User is logged in",headers={"name":"msg"})
                    else:
                        return HTTPException(status_code=200,detail="Password is wrong")
                else:
                    return HTTPException(status_code=204,detail="User not found")
        except Exception as e:
            return HTTPException(status_code=405,detail=f"{e}")
   
    @classmethod 
    def converttoobject(cls,obj):
        return cls (**obj.dict())   

    @classmethod
    def create(cls, userinstance):
        session=next(cls.db())
        userinstance=cls(**userinstance.dict())
        if userinstance and not session.query(User).filter(User.username==userinstance.username.strip().upper()).scalar():
            try:
                session.add(userinstance)
                session.commit()
                session.refresh(userinstance)
                return HTTPException(status_code=200,detail="User created")
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=400, detail=str(e))
            finally:
                session.close()
        else:
            raise HTTPException(status_code=400, detail="User already registered")


    def userexist(self):
        session = next(self.db())
        return HTTPException( status_code=204, detail="User exists" ) if session.query(User).filter(User.username==self.username).scalar() else HTTPException(status_code=404,detail="User Not not found")

    @staticmethod
    def deleteuser(id):
        try:
            if id:
                session=next(User.db())
                user=session.query(User).filter(User.id==id).first()
                if user:
                    session.delete(user)
                    session.commit()
                    return HTTPException(status_code=200,detail="User has been deleted",headers={"msg":[]})
                else:
                    return HTTPException(status_code=404,detail="User not found")
        except Exception as e:
            return HTTPException(status_code=404,detail=f"{e}")
            
Base.metadata.create_all(engine)













