import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)


def test_protected_endpoint_requires_token():
    response = client.get("/books/")
    assert response.status_code == 401


def test_register_and_access():
    # ✅ Генерация уникального email
    email = f"admin_{uuid.uuid4().hex}@test.com"
    password = "test"

    # Регистрация
    response = client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == 200

    # Логин
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Доступ к защищенному эндпоинту
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/books/", headers=headers)
    assert response.status_code in (200, 404)  # 404 если книг нет, 200 если есть
