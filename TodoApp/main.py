from typing import Annotated

import models
from models import Todos

from database import SessionLocal

# from TodoApp.database import SessionLocal

from database import engine


from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

# only runs when todos.db does not exist
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Get methods
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()
