from src.auth.adapters.repositories.mysql_activation_code_repository import (
    MySQLActivationCodeRepository,
)
from src.auth.adapters.repositories.mysql_user_repository import MySQLUserRepository
from src.auth.adapters.services.dummy_email_service import DummyEmailService
from src.auth.core.use_cases.user_activation import UserActivation
from src.auth.core.use_cases.user_authentication import UserAuthentication
from src.auth.core.use_cases.user_registration import UserRegistration
from src.builders.use_cases_builders import (
    get_user_activation_use_case,
    get_user_auth_use_case,
    get_user_registration_use_case,
)


def test_get_user_registration_use_case(mocker):
    mock_connection = mocker.Mock()
    mocker.patch(
        "src.builders.repositories_builders.get_mysql_connection",
        return_value=mock_connection,
    )

    use_case = get_user_registration_use_case()

    assert isinstance(use_case, UserRegistration)
    assert isinstance(use_case.user_repo, MySQLUserRepository)
    assert isinstance(use_case.activation_code_repo, MySQLActivationCodeRepository)
    assert isinstance(use_case.email_service, DummyEmailService)


def test_get_user_verification_use_case(mocker):
    mock_connection = mocker.Mock()
    mocker.patch(
        "src.builders.repositories_builders.get_mysql_connection",
        return_value=mock_connection,
    )

    use_case = get_user_auth_use_case()

    assert isinstance(use_case, UserAuthentication)
    assert isinstance(use_case.user_repo, MySQLUserRepository)


def test_get_user_activation_use_case(mocker):
    mock_connection = mocker.Mock()
    mocker.patch(
        "src.builders.repositories_builders.get_mysql_connection",
        return_value=mock_connection,
    )

    use_case = get_user_activation_use_case()

    assert isinstance(use_case, UserActivation)
    assert isinstance(use_case.user_repo, MySQLUserRepository)
    assert isinstance(use_case.activation_code_repo, MySQLActivationCodeRepository)
