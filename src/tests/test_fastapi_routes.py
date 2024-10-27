import base64

from src.auth.core.domain.user import User
from src.auth.exceptions import BadCredentials, InvalidCode, UserAlreadyExists


def get_auth_headers(username: str, password: str) -> dict:
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {encoded_credentials}"}


def test_register_user_success(client, mock_registration_use_case):
    mock_registration_use_case.execute.return_value = User(
        email="test@test.com", password="test_password", is_active=False
    )
    request_data = {"email": "test@test.com", "password": "test_password"}

    response = client.post("/auth/registration", json=request_data)

    assert response.status_code == 201
    assert response.json() == {"email": "test@test.com", "is_active": False}


def test_activate_user_success(
    client, mock_verification_use_case, mock_activation_use_case
):
    user = User(email="test@test.com", password="test_password", is_active=True)
    mock_verification_use_case.execute.return_value = user
    mock_activation_use_case.execute.return_value = user
    headers = get_auth_headers(username=user.email, password=user.password)
    request_data = {"email": "test@test.com", "code": "test_code"}

    response = client.post("/auth/activation", headers=headers, json=request_data)

    assert response.status_code == 200
    assert response.json() == {"email": "test@test.com", "is_active": True}


def test_user_already_exists_error(client, mock_registration_use_case):
    mock_registration_use_case.execute.side_effect = UserAlreadyExists
    request_data = {"email": "test@test.com", "password": "test_password"}

    response = client.post("/auth/registration", json=request_data)

    assert response.status_code == 400
    assert response.json() == {
        "type": "wrong_email",
        "message": "This email cannot be used.",
    }


def test_bad_credentials(client, mock_verification_use_case):
    user = User(email="test@test.com", password="test_password", is_active=False)
    mock_verification_use_case.execute.side_effect = BadCredentials
    headers = get_auth_headers(username=user.email, password=user.password)
    request_data = {"code": "wrong_code"}

    response = client.post("/auth/activation", headers=headers, json=request_data)

    assert response.status_code == 401
    assert response.json() == {
        "type": "bad_credentials",
        "message": "Unable to log with the provided credentials.",
    }


def test_invalid_code_error(
    client, mock_verification_use_case, mock_activation_use_case
):
    user = User(email="test@test.com", password="test_password", is_active=False)
    mock_verification_use_case.execute.return_value = user
    mock_activation_use_case.execute.side_effect = InvalidCode
    headers = get_auth_headers(username=user.email, password=user.password)
    request_data = {"code": "wrong_code"}

    response = client.post("/auth/activation", headers=headers, json=request_data)

    assert response.status_code == 400
    assert response.json() == {
        "type": "invalid_code",
        "message": "Invalid or expired activation code.",
    }
