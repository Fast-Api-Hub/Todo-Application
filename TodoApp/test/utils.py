from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

SQLACLEHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLACLEHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "user", "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to Code!",
        description="Test description",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE from todos;"))
        conn.commit()


@pytest.fixture
def test_user():
    user = Users(
        id=1,
        emails="test@email.com",
        username="user1",
        first_name="user1",
        last_name="user1",
        hashed_password=bcrypt_context.hash("user1"),
        role="admin",
        phone_number="123456",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE from users"))
        conn.commit()
