from typing import Optional


class User:
    def __init__(
        self, email: str, password: Optional[str] = None, is_active: bool = False
    ):
        self.email = email
        self.password = password
        self.is_active = is_active
