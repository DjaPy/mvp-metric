import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database.db import database
from app import api


current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static"

app = FastAPI()

app.mount('/static', StaticFiles(directory=static_root_absolute), name='static')


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(api.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8899)
