import pytest

from src.auth.core.domain.user import User
from src.auth.core.use_cases.user_activation import UserActivation
from src.auth.exceptions import InvalidCode
from src.auth.ports.repositories.activation_code_repository import (
    AbstractActivationCodeRepository,
)
from src.auth.ports.repositories.user_repository import AbstractUserRepository


def test_user_activation_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=AbstractUserRepository)
    mock_activation_code_repo = mocker.MagicMock(spec=AbstractActivationCodeRepository)
    user = User(email="test@test.com", password="1234", is_active=False)
    mock_user_repo.get_by_email.return_value = user
    mock_activation_code = mocker.MagicMock()
    mock_activation_code.is_code_valid.return_value = True
    mock_activation_code_repo.get_by_email.return_value = mock_activation_code
    user_activation = UserActivation(mock_user_repo, mock_activation_code_repo)

    activated_user = user_activation.execute(user=user, code="12345")

    assert activated_user.is_active
    mock_user_repo.update.assert_called_once_with(user)
    mock_activation_code_repo.get_by_email.assert_called_once_with("test@test.com")


def test_user_activation_invalid_code(mocker):
    mock_user_repo = mocker.MagicMock(spec=AbstractUserRepository)
    mock_activation_code_repo = mocker.MagicMock(spec=AbstractActivationCodeRepository)
    user = User(email="test@test.com", password="password", is_active=False)
    mock_activation_code = mocker.MagicMock()
    mock_activation_code.is_code_valid.return_value = False
    mock_activation_code_repo.get_by_email.return_value = mock_activation_code
    user_activation = UserActivation(mock_user_repo, mock_activation_code_repo)

    with pytest.raises(InvalidCode):
        user_activation.execute(user=user, code="wrong_code")

    mock_activation_code_repo.get_by_email.assert_called_once_with("test@test.com")
