""" Entry Point """
import asyncio
import uvicorn
from fastapi import FastAPI
from core.logging_conf import Logging
from apis.v1 import auth, users, organizations
from db.base import create_db_and_tables
from db.init_db import db_init

log = Logging(__name__).log()

# Create a FastAPI application instance
app = FastAPI()

# Include routers for authentication, users, and organizations APIs
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)

@app.get("/")
async def root():
    """
    Handle the root endpoint.

    Returns:
        dict: A dictionary containing the status of the application.
    """
    log.info("Home Page Called!!!")
    return {"status": "OK"}

def main():
    """
    Entry point for the application.

    This function initializes the database and tables, runs the database initialization script,
    and starts the FastAPI application using Uvicorn.

    Returns:
        None
    """
    create_db_and_tables()
    asyncio.run(db_init())
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
