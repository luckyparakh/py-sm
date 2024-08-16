from app import schemas
from app.config import settings
import jwt
import pytest


def test_root(client):
    response = client.get("/")
    # print(response.json())
    assert response.status_code == 200
    assert response.json().get("message") == "Hello World!!!"


def test_create_user(client):
    test_email = "test@gmail.com"
    response = client.post("/users/", json={
        "email": test_email,
        "password": "password"
    })
    print(response.json())
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == test_email


def test_login(client, test_user):
    print(test_user)
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"],
    })
    assert response.status_code == 200
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
