import pytest

from src.auth.core.domain.user import User
from src.auth.core.use_cases.user_authentication import UserAuthentication
from src.auth.exceptions import BadCredentials, UserNotFound
from src.auth.ports.repositories.user_repository import AbstractUserRepository
from src.auth.ports.services.password_encoder import AbstractPasswordEncoder


def test_user_auth_success(mocker):
    user = User(email="test@test.com", password="password", is_active=False)
    mock_user_repo = mocker.MagicMock(spec=AbstractUserRepository)
    mock_password_encoder = mocker.MagicMock(spec=AbstractPasswordEncoder)
    mock_user_repo.get_by_email.return_value = user
    mock_password_encoder.decode_password.return_value = user.password
    user_verification = UserAuthentication(
        user_repo=mock_user_repo, password_encoder=mock_password_encoder
    )

    verified_user = user_verification.execute(email=user.email, password=user.password)

    assert verified_user == user
    mock_user_repo.get_by_email.assert_called_once_with(
        "test@test.com", with_password=True
    )
    mock_password_encoder.decode_password.assert_called_once()


def test_user_auth_not_found(mocker):
    user = User(email="notfound@test.com", password="password", is_active=False)
    mock_user_repo = mocker.MagicMock(spec=AbstractUserRepository)
    mock_password_encoder = mocker.MagicMock(spec=AbstractPasswordEncoder)
    mock_user_repo.get_by_email.side_effect = UserNotFound
    user_verification = UserAuthentication(
        user_repo=mock_user_repo, password_encoder=mock_password_encoder
    )

    with pytest.raises(BadCredentials):
        user_verification.execute(email="notfound@test.com", password=user.password)

    mock_user_repo.get_by_email.assert_called_once_with(
        "notfound@test.com", with_password=True
    )


def test_user_auth_wrong_password(mocker):
    user = User(email="test@test.com", password="password", is_active=False)
    mock_user_repo = mocker.MagicMock(spec=AbstractUserRepository)
    mock_password_encoder = mocker.MagicMock(spec=AbstractPasswordEncoder)
    mock_user_repo.get_by_email.return_value = user
    user_verification = UserAuthentication(
        user_repo=mock_user_repo, password_encoder=mock_password_encoder
    )

    with pytest.raises(BadCredentials):
        user_verification.execute(email=user.email, password="wrong_password")

    mock_user_repo.get_by_email.assert_called_once_with(
        "test@test.com", with_password=True
    )
    mock_password_encoder.decode_password.assert_called_once()


def test_user_auth_is_valid_password():
    password_1 = "1234"
    password_2 = "1234"
    result = UserAuthentication.is_password_valid(password_1, password_2)
    assert result is True

def test_user_auth_is_not_valid_password():
    password_1 = "1234"
    password_2 = "different"
    result = UserAuthentication.is_password_valid(password_1, password_2)
    assert result is False
