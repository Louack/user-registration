from abc import ABC, abstractmethod
from typing import Optional

from src.auth.core.domain.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def create(self, user: User):
        pass

    @abstractmethod
    def get_by_email(
        self, email: str, with_password: Optional[bool] = False
    ) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User):
        pass
