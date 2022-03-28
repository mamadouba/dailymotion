import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from dailymotion.main import create_app
from tests.mocks import MockRedis, MockSMTPClient
from dailymotion.dependancies import get_db

@pytest.fixture(scope="session", autouse=True)
def initdb():
    db = get_db()
    #db.drop_tables()
    db.create_tables()
    yield db
    db.drop_tables()
    db.close()

@pytest.fixture(scope="session")
def client() -> TestClient:
    app: FastAPI = create_app()
    client = TestClient(app)
    yield client

@pytest.fixture(scope="session")
def mock_redis():
    with patch("dailymotion.dependancies.Redis"):
        return MockRedis()

@pytest.fixture
def mock_smtp():
    with patch("dailymotion.dependancies.SMTPClient"):
        return MockSMTPClient()