from src.auth.ports.services.password_encoder import AbstractPasswordEncoder


class DummyPasswordEncoder(AbstractPasswordEncoder):
    def encode_password(self, password: str) -> str:
        return password

    def decode_password(self, password: str) -> str:
        return password
