from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from main import app, get_db
from models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


SQLModel.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register():
    response = client.post(
        "/api/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login():
    # First, register a user
    client.post(
        "/api/register",
        json={"email": "test2@example.com", "password": "testpassword123"},
    )
    # Then, login
    response = client.post(
        "/api/login",
        json={"email": "test2@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
