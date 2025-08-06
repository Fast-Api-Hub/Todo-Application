from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users

from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_req: CreateUserRequest):
    create_user_model = Users(
        emails=create_user_req.email,
        username=create_user_req.username,
        first_name=create_user_req.first_name,
        last_name=create_user_req.last_name,
        role=create_user_req.role,
        hashed_password=bcrypt_context.hash(create_user_req.hashed_password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()
