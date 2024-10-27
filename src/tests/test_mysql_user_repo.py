import pytest
from mysql.connector import IntegrityError
from mysql.connector.abstracts import MySQLConnectionAbstract

from src.auth.adapters.repositories.mysql_user_repository import MySQLUserRepository
from src.auth.core.domain.user import User
from src.auth.exceptions import UserAlreadyExists, UserNotFound


class TestMySQLUserRepo:
    def test_create_user(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        user = User(email="test@test.com", password="password", is_active=True)

        user_repository = MySQLUserRepository(mock_connection)
        user_repository.create(user)

        mock_cursor.execute.assert_called_once_with(
            operation="INSERT INTO users (email, password, is_active) VALUES (%s, %s, %s)",
            params=(user.email, user.password, user.is_active),
        )
        mock_connection.commit.assert_called_once()

    def test_create_user_already_exists(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.execute.side_effect = IntegrityError
        user = User(email="duplicate@test.com", password="password", is_active=True)

        user_repository = MySQLUserRepository(mock_connection)

        with pytest.raises(UserAlreadyExists):
            user_repository.create(user)

        mock_cursor.execute.assert_called_once_with(
            operation="INSERT INTO users (email, password, is_active) VALUES (%s, %s, %s)",
            params=(user.email, user.password, user.is_active),
        )

    def test_get_by_email_found(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = {"email": "test@test.com", "is_active": 1}

        user_repository = MySQLUserRepository(mock_connection)
        user = user_repository.get_by_email("test@test.com")

        assert user is not None
        assert user.email == "test@test.com"
        assert user.password is None
        assert user.is_active is True
        mock_cursor.execute.assert_called_once_with(
            operation="SELECT email, is_active FROM users WHERE email=%s",
            params=("test@test.com",),
        )

    def test_get_by_email_with_password(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = {
            "email": "test@test.com",
            "password": "1234",
            "is_active": 1,
        }

        user_repository = MySQLUserRepository(mock_connection)
        user = user_repository.get_by_email("test@test.com", with_password=True)

        assert user is not None
        assert user.email == "test@test.com"
        assert user.password == "1234"
        assert user.is_active is True
        mock_cursor.execute.assert_called_once_with(
            operation="SELECT email, password, is_active FROM users WHERE email=%s",
            params=("test@test.com",),
        )

    def test_get_by_email_not_found(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None

        user_repository = MySQLUserRepository(mock_connection)
        with pytest.raises(UserNotFound):
            user_repository.get_by_email("test@test.com")

        mock_cursor.execute.assert_called_once_with(
            operation="SELECT email, is_active FROM users WHERE email=%s",
            params=("test@test.com",),
        )

    def test_update_user(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        user = User(email="test@test.com", password="password", is_active=False)

        user_repository = MySQLUserRepository(mock_connection)
        user_repository.update(user)

        mock_cursor.execute.assert_called_once_with(
            operation="UPDATE users SET is_active=%s WHERE email=%s",
            params=(user.is_active, user.email),
        )
        mock_connection.commit.assert_called_once()
