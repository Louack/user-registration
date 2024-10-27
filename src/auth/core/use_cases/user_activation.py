from src.auth.core.domain.user import User
from src.auth.exceptions import InvalidCode
from src.auth.ports.repositories.activation_code_repository import (
    AbstractActivationCodeRepository,
)
from src.auth.ports.repositories.user_repository import AbstractUserRepository


class UserActivation:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        activation_code_repo: AbstractActivationCodeRepository,
    ):
        self.user_repo = user_repo
        self.activation_code_repo = activation_code_repo

    def execute(self, user: User, code: str) -> User:
        activation_code = self.activation_code_repo.get_by_email(user.email)

        if not activation_code.is_code_valid(input_code=code):
            raise InvalidCode

        user.is_active = True
        self.user_repo.update(user)

        return user
