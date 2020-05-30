import uvicorn

from fastapi import FastAPI

from app.database.db import database
from app import api


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(api.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8899)
