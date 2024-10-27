from src import settings
from src.auth.core.use_cases.user_activation import UserActivation
from src.auth.core.use_cases.user_authentication import UserAuthentication
from src.auth.core.use_cases.user_registration import UserRegistration
from src.builders.repositories_builders import (
    get_mysql_activation_code_repository,
    get_mysql_user_repository,
)
from src.builders.services_builders import (
    get_dummy_email_service,
    get_dummy_password_encoder,
)

USER_REPOSITORIES = {"mysql_user_repo": get_mysql_user_repository}
ACTIVATION_CODE_REPOSITORIES = {
    "mysql_activation_code_repo": get_mysql_activation_code_repository
}

PASSWORD_ENCODERS = {"dummy_password_encoder": get_dummy_password_encoder}
EMAIL_SERVICES = {"dummy_email_service": get_dummy_email_service}


def get_user_registration_use_case() -> UserRegistration:
    user_repo = USER_REPOSITORIES.get(settings.USER_REPO)()
    activation_code_repo = ACTIVATION_CODE_REPOSITORIES.get(
        settings.ACTIVATION_CODE_REPO
    )()
    password_encoder = PASSWORD_ENCODERS.get(settings.PASSWORD_ENCODER)()
    email_service = EMAIL_SERVICES.get(settings.EMAIL_SERVICE)()
    return UserRegistration(
        user_repo=user_repo,
        activation_code_repo=activation_code_repo,
        password_encoder=password_encoder,
        email_service=email_service,
    )


def get_user_auth_use_case() -> UserAuthentication:
    user_repo = USER_REPOSITORIES.get(settings.USER_REPO)()
    password_encoder = PASSWORD_ENCODERS.get(settings.PASSWORD_ENCODER)()
    return UserAuthentication(user_repo=user_repo, password_encoder=password_encoder)


def get_user_activation_use_case() -> UserActivation:
    user_repo = USER_REPOSITORIES.get(settings.USER_REPO)()
    activation_code_repo = ACTIVATION_CODE_REPOSITORIES.get(
        settings.ACTIVATION_CODE_REPO
    )()
    return UserActivation(
        user_repo=user_repo,
        activation_code_repo=activation_code_repo,
    )
