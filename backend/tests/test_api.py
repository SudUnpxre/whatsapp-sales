import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config_test import settings
from app.models.models import User
from app.core.security import get_password_hash

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db(client):
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(db: Session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        whatsapp_number="+5511999999999"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "WhatsApp Sales Automation API"}

def test_create_user(client, db):
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "email": "newuser@example.com",
            "password": "newpassword",
            "full_name": "New User",
            "whatsapp_number": "+5511988888888"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data

def test_login(client, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me(client, test_user):
    # Primeiro fazer login
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword"
        },
    )
    token = login_response.json()["access_token"]
    
    # Tentar acessar /me
    response = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User" 