import pytest
from fastapi import status
from starlette.testclient import TestClient
from main import app
from repository.auth_repo import create_access_token, verify_token
from datetime import timedelta
from schemas import CreateUser

client = TestClient(app)

user_data = {
    "email": "test@example.com",
    "password": "testpassword",
    "full_name": "Test User",
}

token_data = {"sub": "test@example.com", "id": 1}

test_access_token = create_access_token(
    data=token_data, expires_delta=timedelta(minutes=1)
)


def test_create_user():
    response = client.post("/user/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == user_data["email"]
    assert "id" in response.json()


def test_get_user():
    create_user_response = client.post("/user/", json=user_data)
    created_user_id = create_user_response.json()["id"]

    response = client.get(
        f"/user/{created_user_id}",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user_data["email"]
    assert response.json()["id"] == created_user_id


def test_update_user():
    create_user_response = client.post("/user/", json=user_data)
    created_user_id = create_user_response.json()["id"]

    new_full_name = "Updated User"
    update_data = {"full_name": new_full_name}
    response = client.patch(
        f"/user/{created_user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["full_name"] == new_full_name


def test_delete_user():
    create_user_response = client.post("/user/", json=user_data)
    created_user_id = create_user_response.json()["id"]

    response = client.delete(
        f"/user/{created_user_id}",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK


def test_verify_token():
    verify_token(test_access_token, credentials_exception=None)


def test_invalid_token():
    with pytest.raises(Exception):
        invalid_token = "invalid_token"
        verify_token(invalid_token, credentials_exception=None)
