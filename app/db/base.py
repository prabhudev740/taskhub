from fastapi import Depends
from core.config import DATABASE_URL
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session


Base = declarative_base()

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)

def create_db_and_tables():
    Base.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        return session

SessionDep = Annotated[Session, Depends(get_session)]
