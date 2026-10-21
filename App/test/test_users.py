import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from App.DataBase import get_db
from App.main import app
from App.models import Base
from App.dependencies import get_current_user


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

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


def test_user_registration_uses_isolated_database(client):
    response = client.post(
        "/users/",
        json={
            "user_name": "newuser",
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "user_id": 1,
        "user_name": "newuser",
        "email": "newuser@example.com",
    }


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
