""" Base DB """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from core.config import DATABASE_URL

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Connection arguments for the SQLite database
connect_args = {"check_same_thread": False}

# Create a SQLAlchemy engine with specific configurations
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Maximum number of connections that can be created beyond the pool size
    pool_timeout=30,  # Timeout in seconds for acquiring a connection from the pool
    connect_args=connect_args,  # Additional connection arguments
    echo=True  # Enable SQL query logging
)

def get_session():
    """
    Create and return a new SQLAlchemy session.

    This function uses the configured engine to create a session
    for interacting with the database.

    Returns:
        sqlalchemy.orm.Session: A new session instance.
    """
    with Session(engine) as session:
        return session

def create_db_and_tables():
    """
    Create all database tables defined in the SQLAlchemy models.

    This function uses the metadata of the `Base` class to create
    tables in the database connected to the engine.
    """
    Base.metadata.create_all(engine)

# async def get_session():
#     """
#     Create and yield an asynchronous SQLAlchemy session.

#     This function uses the configured engine to create an async session
#     for interacting with the database.

#     Yields:
#         sqlalchemy.ext.asyncio.AsyncSession: An async session instance.
#     """
#     async with AsyncSession(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_session)]
