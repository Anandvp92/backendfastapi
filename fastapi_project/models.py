from database import Base,engine
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from database import session_local
from fastapi import HTTPException
from passlib.context import CryptContext


SECRET_KEY ="b360aa7d2fa355afa670ad2480d0b18d931a4f1049413230c6020f5731345f44"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class User(Base):
    __tablename__="User"
    id = Column("User_ID",Integer,primary_key=True,index=True)
    username=Column("Username",String(225),unique=True,nullable=False)
    email=Column("Email",String(225),unique=True,nullable=False)
    phonenumber=Column("Phone_number",Integer,unique=True,nullable=False)
    password=Column("Password",String(50))
    is_admin=Column("Is_admin",Boolean,default=False)
    is_staff=Column("Is_staff",Boolean,default=True)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
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
    def verify(cls,instance):
        return pwd_context.verify(self.password,instance.password)

    @classmethod 
    def converttoobject(cls,obj):
        return cls (**obj.dict())   


    @classmethod
    def create(cls,userinstance):
        session=session_local()
        userinstance=cls(**userinstance.dict())
        if userinstance:
                try:
                    session.add(userinstance)
                    session.commit()
                    session.refresh(userinstance)
                    return HTTPException(status_code=200,detail="User created sucessfully")
                except Exception as e:
                    session.rollback()
                    raise e
                finally:
                    session.close()

        else:
            return  HTTPException(status_code=200,detail="Something went Wrong")

    def userexist(self):
        session = next(self.db())
        return "User exists" if session.query(User).filter(User.username==self.username).scalar() else "Not"


Base.metadata.create_all(engine)













