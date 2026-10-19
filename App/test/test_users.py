from ast import PyCF_TYPE_COMMENTS
import os
import pytest

os.environ["TEST_DB_NAME"] = "airesearchhub_test"

from fastapi.testclient import TestClient
from main import app
from dependencies import get_current_user


@pytest.fixture
def client():
    yield TestClient(app)
    app.dependency_overrides.clear()    

def test_users_me_require_auth(client):
    respone = client.get("/users/me")
    assert respone.status_code == 401

    assert respone.json() == {"detail": "Not authenticated"}

def test_users_me_with_authenticated_user(client):
    class FakeUser:
        user_id = 1
        user_name = "testuser"
        email = "test@example.com"

    app.dependency_overrides[get_current_user] = lambda: FakeUser()

    try:
        response = client.get("/users/me")
        assert response.status_code == 200
        assert response.json()["user_name"] == "testuser"
    finally:
        app.dependency_overrides.clear()


def test_login_invalid_credentials(client):
    response = client.post(
        "/users/login",
        json={
            "email": "nobody_exists@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
