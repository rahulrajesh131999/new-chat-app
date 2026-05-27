from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def getSession():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(getSession)]