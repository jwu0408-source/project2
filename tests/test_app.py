import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///test_contact_app.db")

from contact_app.main import app


@pytest.fixture()
def client():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
        from contact_app import database

        database.engine.dispose()
        database.Base.metadata.drop_all(bind=database.engine)
        database.Base.metadata.create_all(bind=database.engine)

        with TestClient(app) as test_client:
            yield test_client


def test_signup_login_and_contacts_flow(client):
    signup_response = client.post(
        "/auth/signup",
        json={"username": "happyday", "password": "1234"},
    )
    assert signup_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"username": "happyday", "password": "1234"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    category_response = client.post(
        "/categories",
        json={"name": "친구"},
        headers=headers,
    )
    assert category_response.status_code == 201

    contact_response = client.post(
        "/contacts",
        json={
            "name": "윤아",
            "phone": "01012345678",
            "addr": "서울",
            "category_id": category_response.json()["id"],
        },
        headers=headers,
    )
    assert contact_response.status_code == 201

    contacts_response = client.get("/contacts", headers=headers)
    assert contacts_response.status_code == 200
    data = contacts_response.json()
    assert data[0]["name"] == "윤아"


def test_login_failure_returns_unauthorized_and_delete_returns_no_content(client):
    signup_response = client.post(
        "/auth/signup",
        json={"username": "tester", "password": "1234"},
    )
    assert signup_response.status_code == 201

    failed_login_response = client.post(
        "/auth/login",
        json={"username": "tester", "password": "wrong"},
    )
    assert failed_login_response.status_code == 401

    login_response = client.post(
        "/auth/login",
        json={"username": "tester", "password": "1234"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    category_response = client.post(
        "/categories",
        json={"name": "가족"},
        headers=headers,
    )
    assert category_response.status_code == 201

    contact_response = client.post(
        "/contacts",
        json={
            "name": "민수",
            "phone": "01011112222",
            "addr": "부산",
            "category_id": category_response.json()["id"],
        },
        headers=headers,
    )
    assert contact_response.status_code == 201

    delete_response = client.delete(f"/contacts/{contact_response.json()['id']}", headers=headers)
    assert delete_response.status_code == 204
    assert delete_response.content == b""


def test_update_contact(client):
    signup_response = client.post(
        "/auth/signup",
        json={"username": "updater", "password": "1234"},
    )
    assert signup_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"username": "updater", "password": "1234"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    contact_response = client.post(
        "/contacts",
        json={
            "name": "철수",
            "phone": "01055556666",
            "addr": "서울",
        },
        headers=headers,
    )
    assert contact_response.status_code == 201
    contact_id = contact_response.json()["id"]

    update_response = client.patch(
        f"/contacts/{contact_id}",
        json={"name": "영수", "addr": "인천"},
        headers=headers,
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "영수"
    assert data["addr"] == "인천"
    assert data["phone"] == "01055556666"

    contact2_response = client.post(
        "/contacts",
        json={
            "name": "영미",
            "phone": "01077778888",
            "addr": "대구",
        },
        headers=headers,
    )
    assert contact2_response.status_code == 201

    duplicate_phone_response = client.patch(
        f"/contacts/{contact_id}",
        json={"phone": "01077778888"},
        headers=headers,
    )
    assert duplicate_phone_response.status_code == 409
    assert duplicate_phone_response.json()["detail"] == "duplicate phone number"
