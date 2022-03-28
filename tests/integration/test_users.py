import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from tests.mocks import MockRedis, MockSMTPClient

userCreatePayload = {"email": "test1@example.com", "password": "123Aze!"}

redis_cache = {}


def test_create_user(client: TestClient, mock_smtp, mock_redis):
    """test create user"""
    response = client.post("/users/", json=userCreatePayload)
    print(response.json())
    print(mock_redis.cache)
    assert response.status_code == 201
    assert response.json() == {
        "message": "Your activation code has been sent to the email you have provided"
    }


def test_list_users(client: TestClient):
    """test list users"""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data[-1]
    pytest.user_id = data[-1]["id"]


def test_get_user(client: TestClient):
    """test get user"""
    response = client.get(f"/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "new"
    assert data["email"] == userCreatePayload["email"]


def test_activate_user(client: TestClient, mock_smtp, mock_redis):
    """test activate user"""
    # print(mock_redis.cache)
    payload = {
        "email": userCreatePayload["email"],
        "code": redis_cache.get(f"activation_codes/{userCreatePayload['email']}"),
    }

    response = client.post(f"/users/activate", json=payload)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_delete_user(client: TestClient):
    """test delete user"""
    response = client.delete(f"/users/1")
    assert response.status_code == 200
    data = response.json()
