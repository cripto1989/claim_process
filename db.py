from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

from config import get_settings

settings = get_settings()

DB_URL = settings.DATABASE_URL

engine = create_engine(DB_URL)


def create_all_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
