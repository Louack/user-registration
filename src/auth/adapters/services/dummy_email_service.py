from src.auth.ports.services.email_service import AbstractEmailService


class DummyEmailService(AbstractEmailService):
    def send_activation_code(self, email: str, code: str):
        print(f"Activation code '{code}' sent to {email}...")
