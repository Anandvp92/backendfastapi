from database import Base,engine
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from database import session_local
from fastapi import HTTPException
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

    @staticmethod
    def db():
        session = session_local()
        try:
            yield session
        finally:
            session.close()

            


    @classmethod
    def create(cls,userinstance):
        session=session_local()
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
       return db.query(User).filter(User.username==self.username).scalar()


Base.metadata.create_all(engine)













