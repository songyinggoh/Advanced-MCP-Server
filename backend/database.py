from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

engine=create_engine('sqlite:///database.db')
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

#define the python object that will be mapped to sql 
class Note(Base):
    __tablename__="notes"

    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(String, nullable=False, index=True)
    content=Column(Text, nullable=False)


Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()