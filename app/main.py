import asyncio
import uvicorn
from fastapi import FastAPI
from core.logging_conf import Logging
from apis.v1 import auth, users, organizations
from db.base import create_db_and_tables
from db.init_db import db_init

log = Logging(__name__).log()

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)

@app.get("/")
async def root():
    log.info("Home Page Called!!1")
    return {"status": "OK"}

def main():
    create_db_and_tables()
    asyncio.run(db_init())


if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)