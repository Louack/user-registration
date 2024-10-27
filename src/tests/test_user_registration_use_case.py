from src.auth.core.use_cases.user_registration import UserRegistration
from src.auth.ports.repositories.activation_code_repository import (
    AbstractActivationCodeRepository,
)
from src.auth.ports.repositories.user_repository import AbstractUserRepository
from src.auth.ports.services.email_service import AbstractEmailService
from src.auth.ports.services.password_encoder import AbstractPasswordEncoder


def test_user_registration_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=AbstractUserRepository)
    mock_activation_code_repo = mocker.MagicMock(spec=AbstractActivationCodeRepository)
    mock_password_encoder = mocker.MagicMock(spec=AbstractPasswordEncoder)
    mock_email_service = mocker.MagicMock(spec=AbstractEmailService)

    user_registration = UserRegistration(
        user_repo=mock_user_repo,
        activation_code_repo=mock_activation_code_repo,
        password_encoder=mock_password_encoder,
        email_service=mock_email_service,
    )

    registered_user = user_registration.execute(
        email="test@test.com", password="password"
    )
    activation_code_obj = mock_activation_code_repo.create.call_args[1][
        "activation_code"
    ]

    assert registered_user.email == "test@test.com"
    assert registered_user.is_active is False
    mock_user_repo.create.assert_called_once_with(user=registered_user)
    mock_password_encoder.encode_password.assert_called_once_with("password")
    mock_email_service.send_activation_code.assert_called_once_with(
        "test@test.com", activation_code_obj.code
    )
