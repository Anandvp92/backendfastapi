from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session,sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./backend.db",echo=True)

Base = declarative_base()

session_local = sessionmaker(bind=engine)



