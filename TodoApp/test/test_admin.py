from .utils import *

from ..routers.admin import get_db, get_current_user
from ..models import Todos

from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "complete": False,
        "description": "Test description",
        "id": 1,
        "owner_id": 1,
        "priority": 5,
        "title": "Learn to Code!",
    }]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_todo_not_exist(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == 401
    assert response.json() == {"detail": "Todo not found."}
