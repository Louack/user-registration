from abc import ABC, abstractmethod


class AbstractPasswordEncoder(ABC):
    @abstractmethod
    def encode_password(self, password: str) -> str:
        pass

    @abstractmethod
    def decode_password(self, password: str) -> str:
        pass
