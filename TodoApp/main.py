import models
from database import engine
from routers import auth, todos, admin

from fastapi import FastAPI

app = FastAPI()
# only runs when todos.db does not exist
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
