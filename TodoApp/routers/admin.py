from typing import Annotated

from pydantic import BaseModel, Field
from starlette import status

from ..models import Todos, Users
from ..database import SessionLocal

from fastapi import Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session

from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# GET Request
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed.")

    return db.query(Todos).all()


# DELETE Request
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed.")

    admin_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if admin_model is None:
        raise HTTPException(status_code=401, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
