from src.auth.adapters.services.dummy_email_service import DummyEmailService
from src.auth.adapters.services.dummy_password_encoder import DummyPasswordEncoder


def get_dummy_email_service() -> DummyEmailService:
    return DummyEmailService()


def get_dummy_password_encoder() -> DummyPasswordEncoder:
    return DummyPasswordEncoder()
