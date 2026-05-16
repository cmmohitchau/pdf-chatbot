from config.config import DATABASE_URL
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends


engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
    