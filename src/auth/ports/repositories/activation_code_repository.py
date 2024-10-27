from abc import ABC, abstractmethod
from typing import Optional

from src.auth.core.domain.user_activation_code import UserActivationCode


class AbstractActivationCodeRepository(ABC):
    @abstractmethod
    def create(self, activation_code: UserActivationCode):
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserActivationCode]:
        pass
