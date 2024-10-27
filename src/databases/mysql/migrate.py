import os
import time

import mysql.connector
from mysql.connector import DatabaseError
from mysql.connector import Error as MySQLError

from src import settings
from src.databases.mysql.connection import get_mysql_connection


def apply_migration(migration_file):
    with open(migration_file, "r") as file:
        sql = file.read()

    with get_mysql_connection(
        db_host=settings.MYSQL_DB_HOST,
        db_name=settings.MYSQL_DB_NAME,
        db_user=settings.MYSQL_DB_USER,
        db_password=settings.MYSQL_DB_PASSWORD,
    ) as db_connection:
        with db_connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                db_connection.commit()
                print(f"Applied migration: {migration_file}")
            except mysql.connector.Error as err:
                print(f"Error applying migration {migration_file}: {err}")


def migrate():
    retries = 10
    while retries:
        try:
            migrations_directory = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "migrations"
            )
            migration_files = sorted(os.listdir(migrations_directory))

            for migration_file in migration_files:
                apply_migration(os.path.join(migrations_directory, migration_file))
            return
        except MySQLError:
            time.sleep(2)
            retries -= 1
    raise DatabaseError


if __name__ == "__main__":
    migrate()
