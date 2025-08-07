from ..database import Base
from ..main import app
from ..models import Todos

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
