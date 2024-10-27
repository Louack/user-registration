from src.auth.core.domain.user import User
from src.auth.core.domain.user_activation_code import UserActivationCode
from src.auth.ports.repositories.activation_code_repository import (
    AbstractActivationCodeRepository,
)
from src.auth.ports.repositories.user_repository import AbstractUserRepository
from src.auth.ports.services.email_service import AbstractEmailService
from src.auth.ports.services.password_encoder import AbstractPasswordEncoder


class UserRegistration:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        activation_code_repo: AbstractActivationCodeRepository,
        password_encoder: AbstractPasswordEncoder,
        email_service: AbstractEmailService,
    ):
        self.user_repo = user_repo
        self.activation_code_repo = activation_code_repo
        self.password_encoder = password_encoder
        self.email_service = email_service

    def execute(self, email: str, password: str) -> User:
        encoded_password = self.password_encoder.encode_password(password)

        user = User(email=email, password=encoded_password, is_active=False)
        self.user_repo.create(user=user)

        activation_code = UserActivationCode.create(email=email)
        self.activation_code_repo.create(activation_code=activation_code)

        self.email_service.send_activation_code(user.email, activation_code.code)

        return user
