import random
import string
from datetime import datetime, timedelta


class UserActivationCode:
    def __init__(self, email: str, code: str, expiry_date: datetime):
        self.email = email
        self.code = code
        self.expiry_date = expiry_date

    @classmethod
    def create(cls, email: str):
        code = "".join(random.choices(string.digits, k=4))
        expiry_date = datetime.now() + timedelta(minutes=1)
        return cls(email=email, code=code, expiry_date=expiry_date)

    def is_code_valid(self, input_code: str) -> bool:
        return self.code == input_code and self.expiry_date >= datetime.now()
