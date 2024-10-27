from src import settings
from src.auth.adapters.repositories.mysql_activation_code_repository import (
    MySQLActivationCodeRepository,
)
from src.auth.adapters.repositories.mysql_user_repository import MySQLUserRepository
from src.databases.mysql.connection import get_mysql_connection


def get_mysql_user_repository() -> MySQLUserRepository:
    connection = get_mysql_connection(
        db_host=settings.MYSQL_DB_HOST,
        db_name=settings.MYSQL_DB_NAME,
        db_user=settings.MYSQL_DB_USER,
        db_password=settings.MYSQL_DB_PASSWORD,
    )
    return MySQLUserRepository(connection=connection)


def get_mysql_activation_code_repository() -> MySQLActivationCodeRepository:
    connection = get_mysql_connection(
        db_host=settings.MYSQL_DB_HOST,
        db_name=settings.MYSQL_DB_NAME,
        db_user=settings.MYSQL_DB_USER,
        db_password=settings.MYSQL_DB_PASSWORD,
    )
    return MySQLActivationCodeRepository(connection=connection)
