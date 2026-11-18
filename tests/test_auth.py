import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def registered_user():
    # Generate a unique email so tests can be repeated
    email = f"pytest_{uuid.uuid4().hex[:10]}@example.com"
    password = "TestPass123"

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Pytest User",
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200

    return {
        "email": email,
        "password": password,
        "user_id": response.json()["user_id"]
    }


def test_user_registration(registered_user):
    assert registered_user["user_id"] > 0


def test_duplicate_email_registration(registered_user):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Another User",
            "email": registered_user["email"],
            "password": "AnotherPass123"
        }
    )

    assert response.status_code == 409


def test_registration_validation():
    response = client.post(
        "/auth/register",
        json={
            "full_name": "A",
            "email": "test@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 422


def test_successful_login(registered_user):
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful!"
    assert "access_token" in response.json()


def test_login_with_wrong_password(registered_user):
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": "WrongPass123"
        }
    )

    assert response.status_code == 401


def test_protected_profile_without_token():
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_protected_profile_with_token(registered_user):
    login_response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == registered_user["email"]