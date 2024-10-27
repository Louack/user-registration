from src.auth.core.domain.user import User
from src.auth.exceptions import BadCredentials, UserNotFound
from src.auth.ports.repositories.user_repository import AbstractUserRepository
from src.auth.ports.services.password_encoder import AbstractPasswordEncoder


class UserAuthentication:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        password_encoder: AbstractPasswordEncoder,
    ):
        self.user_repo = user_repo
        self.password_encoder = password_encoder

    def execute(self, email: str, password: str) -> User:
        try:
            user = self.user_repo.get_by_email(email, with_password=True)
        except UserNotFound:
            raise BadCredentials

        decoded_password = self.password_encoder.decode_password(user.password)

        if not self.is_password_valid(decoded_password, password):
            raise BadCredentials

        user.password = None

        return user

    @staticmethod
    def is_password_valid(password1: str, password2: str) -> bool:
        return password1 == password2