from mysql.connector import connect
from mysql.connector.abstracts import MySQLConnectionAbstract


def get_mysql_connection(
    db_host: str, db_name: str, db_user: str, db_password: str
) -> MySQLConnectionAbstract:
    return connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )
