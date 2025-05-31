import uvicorn
from fastapi import FastAPI

from core.logging_conf import Logging
from apis.v1 import auth, users

log = Logging(__name__).log()

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    log.info("Home Page Called!!1")
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)