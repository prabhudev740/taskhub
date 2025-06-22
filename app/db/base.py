from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from core.config import DATABASE_URL


Base = declarative_base()

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)

def get_session():
    with Session(engine) as session:
        return session


def create_db_and_tables():
    Base.metadata.create_all(engine)


# TODO: Implement Async session
# async def get_session():
#     async with AsyncSession(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]
