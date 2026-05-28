from fastapi import FastAPI;
from contextlib import asynccontextmanager

from core.db import create_db_and_tables
from middleware import middleware


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("connected to db")
    create_db_and_tables()
    yield
    print("shutting down")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message":"this is home page"}