from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.v0_router import v0_router
from .persistence.engine import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Nacon interview project.",
    description="Mini game content manager.",
    lifespan=lifespan,
)

app.include_router(router=v0_router, prefix="/api")


@app.get("/")
async def hello_world():
    return {"Hello": "world!"}
