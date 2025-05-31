from fastapi import Depends
from core.config import DATABASE_URL
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)

Base = declarative_base()

def create_db_and_tables():
    Base.metadata.create_all(engine)

def get_session():
    with sessionmaker(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
