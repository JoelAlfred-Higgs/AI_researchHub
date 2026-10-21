import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import Mock

from App.DataBase import get_db
from App.DataBase import ConfigurationError as DatabaseConfigurationError
from App.DataBase import validate_database_config
from App.main import app
from App.models import Base
from App.dependencies import get_current_user
from App.crud import adduser
from App.schemas import CreateUser
from App.security import ConfigurationError as SecurityConfigurationError
from App.security import validate_security_config


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


def test_email_addresses_are_normalized_for_registration_and_login(client):
    registration = client.post(
        "/users/",
        json={
            "user_name": "alice",
            "email": "Alice@Example.COM",
            "password": "SecurePassword123!",
        },
    )
    assert registration.status_code == 201
    assert registration.json()["email"] == "alice@example.com"

    duplicate = client.post(
        "/users/",
        json={
            "user_name": "another-alice",
            "email": "alice@example.com",
            "password": "SecurePassword123!",
        },
    )
    assert duplicate.status_code == 409
    assert duplicate.json() == {"detail": "User already exists!"}

    login = client.post(
        "/users/login",
        json={"email": "ALICE@example.com", "password": "SecurePassword123!"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"


def test_registration_integrity_error_is_reported_as_duplicate():
    db = Mock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.commit.side_effect = IntegrityError("insert", {}, Exception("duplicate key"))
    user = CreateUser(
        user_name="race-user",
        email="race@example.com",
        password="SecurePassword123!",
    )

    assert adduser(user, db) is None
    db.rollback.assert_called_once()


def test_missing_security_configuration_is_a_clear_validation_error(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(SecurityConfigurationError, match="JWT_SECRET_KEY"):
        validate_security_config()


def test_missing_database_configuration_is_a_clear_validation_error(monkeypatch):
    for name in ("DATABASE_URL", "TEST_DB_NAME", "DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(DatabaseConfigurationError, match="Missing database configuration"):
        validate_database_config()


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
