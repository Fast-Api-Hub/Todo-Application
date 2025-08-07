from ..main import app
from ..database import Base
from ..models import Todos

from ..routers.todos import get_db, get_current_user

import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi import status
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


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "description": "Test description",
            "id": 1,
            "owner_id": 1,
            "priority": 5,
            "title": "Learn to Code!",
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False,
        "description": "Test description",
        "id": 1,
        "owner_id": 1,
        "priority": 5,
        "title": "Learn to Code!",
    }


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}


def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo!",
        "description": "New description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todo", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title": "New Todo! UPDATED!",
        "description": "New description  UPDATED!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "New Todo! UPDATED!",
        "description": "New description  UPDATED!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model == None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
