from datetime import datetime

import pytest
from mysql.connector import IntegrityError
from mysql.connector.abstracts import MySQLConnectionAbstract

from src.auth.adapters.repositories.mysql_activation_code_repository import (
    MySQLActivationCodeRepository,
)
from src.auth.core.domain.user_activation_code import UserActivationCode
from src.auth.exceptions import UserAlreadyExists, UserNotFound


class TestMySQLActivationCodeRepo:
    def test_create_activation_code(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        activation_code = UserActivationCode(
            email="test@test.com", code="code", expiry_date=datetime.now()
        )

        activation_code_repo = MySQLActivationCodeRepository(mock_connection)
        activation_code_repo.create(activation_code)

        mock_cursor.execute.assert_called_once_with(
            operation="INSERT INTO activation_codes (email, code, expiry_date) VALUES (%s, %s, %s)",
            params=(
                activation_code.email,
                activation_code.code,
                activation_code.expiry_date,
            ),
        )
        mock_connection.commit.assert_called_once()

    def test_create_activation_code_already_exists(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.execute.side_effect = IntegrityError
        activation_code = UserActivationCode(
            email="test@test.com", code="code", expiry_date=datetime.now()
        )

        activation_code_repo = MySQLActivationCodeRepository(mock_connection)

        with pytest.raises(UserAlreadyExists):
            activation_code_repo.create(activation_code)

    def test_get_by_email_found(self, mocker):
        date = datetime.now()
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = {
            "email": "test@test.com",
            "code": "1234",
            "expiry_date": date,
        }

        activation_code_repo = MySQLActivationCodeRepository(mock_connection)
        activation_code = activation_code_repo.get_by_email("test@test.com")

        assert activation_code is not None
        assert activation_code.email == "test@test.com"
        assert activation_code.code == "1234"
        assert activation_code.expiry_date == date
        mock_cursor.execute.assert_called_once_with(
            operation="SELECT email, code, expiry_date FROM activation_codes WHERE email=%s",
            params=("test@test.com",),
        )

    def test_get_by_email_not_found(self, mocker):
        mock_connection = mocker.MagicMock(spec=MySQLConnectionAbstract)
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None

        activation_code_repo = MySQLActivationCodeRepository(mock_connection)
        with pytest.raises(UserNotFound):
            activation_code_repo.get_by_email("test@test.com")

        mock_cursor.execute.assert_called_once_with(
            operation="SELECT email, code, expiry_date FROM activation_codes WHERE email=%s",
            params=("test@test.com",),
        )
