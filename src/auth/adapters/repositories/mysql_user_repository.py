from typing import Optional

from mysql.connector import IntegrityError
from mysql.connector.abstracts import MySQLConnectionAbstract

from src.auth.core.domain.user import User
from src.auth.exceptions import UserAlreadyExists, UserNotFound
from src.auth.ports.repositories.user_repository import AbstractUserRepository


class MySQLUserRepository(AbstractUserRepository):
    def __init__(self, connection: MySQLConnectionAbstract):
        self.connection = connection

    def create(self, user: User):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    operation="INSERT INTO users (email, password, is_active) VALUES (%s, %s, %s)",
                    params=(user.email, user.password, user.is_active),
                )
                self.connection.commit()
            except IntegrityError:
                raise UserAlreadyExists

    def get_by_email(
        self, email: str, with_password: Optional[bool] = False
    ) -> Optional[User]:
        operation = "SELECT email, is_active FROM users WHERE email=%s"
        if with_password:
            operation = "SELECT email, password, is_active FROM users WHERE email=%s"

        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(operation=operation, params=(email,))
            row = cursor.fetchone()

            if not row:
                raise UserNotFound

            if not row.get("password"):
                row["password"] = None

            user = User(
                email=row["email"],
                password=row["password"],
                is_active=bool(row["is_active"]),
            )
            return user

    def update(self, user: User):
        with self.connection.cursor() as cursor:
            cursor.execute(
                operation="UPDATE users SET is_active=%s WHERE email=%s",
                params=(user.is_active, user.email),
            )
            self.connection.commit()
