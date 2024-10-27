from abc import ABC, abstractmethod


class AbstractEmailService(ABC):
    @abstractmethod
    def send_activation_code(self, email: str, code: str):
        pass
