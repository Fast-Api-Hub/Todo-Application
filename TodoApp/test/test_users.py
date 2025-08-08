from .utils import *
from ..routers.users import get_db, get_current_user

from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users")

    assert response.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["emails"] == "test@email.com"
    assert response.json()["username"] == "user1"
    assert response.json()["first_name"] == "user1"
    assert response.json()["last_name"] == "user1"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "123456"


def test_change_password_sucess(test_user):
    response = client.put(
        "/users/password", json={"password": "user1", "new_password": "user2"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_fail(test_user):
    response = client.put(
        "/users/password", json={"password": "user999", "new_password": "user2"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_password_phone_number_sucess(test_user):
    response = client.put("/users/phonenumber/222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
