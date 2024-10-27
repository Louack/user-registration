from typing import Optional

from mysql.connector import IntegrityError
from mysql.connector.abstracts import MySQLConnectionAbstract

from src.auth.core.domain.user_activation_code import UserActivationCode
from src.auth.exceptions import UserAlreadyExists, UserNotFound
from src.auth.ports.repositories.activation_code_repository import (
    AbstractActivationCodeRepository,
)


class MySQLActivationCodeRepository(AbstractActivationCodeRepository):
    def __init__(self, connection: MySQLConnectionAbstract):
        self.connection = connection

    def create(self, activation_code: UserActivationCode):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    operation="INSERT INTO activation_codes (email, code, expiry_date) VALUES (%s, %s, %s)",
                    params=(
                        activation_code.email,
                        activation_code.code,
                        activation_code.expiry_date,
                    ),
                )
                self.connection.commit()
            except IntegrityError:
                raise UserAlreadyExists

    def get_by_email(self, email: str) -> Optional[UserActivationCode]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                operation="SELECT email, code, expiry_date FROM activation_codes WHERE email=%s",
                params=(email,),
            )
            row = cursor.fetchone()

            if not row:
                raise UserNotFound

            activation_code = UserActivationCode(
                row["email"], row["code"], row["expiry_date"]
            )
            return activation_code
