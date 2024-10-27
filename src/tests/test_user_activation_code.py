from datetime import datetime, timedelta

from pytest import fixture

from src.auth.core.domain.user_activation_code import UserActivationCode


@fixture()
def user_activation_code():
    return UserActivationCode(
        email="test@test.com",
        code="1234",
        expiry_date=datetime.now() + timedelta(minutes=1),
    )


class TestUserActivationCode:
    def test_create_new_code(self):
        new_code = UserActivationCode.create(email="test@test.com")
        assert new_code.email == "test@test.com"
        assert len(new_code.code) == 4
        assert all(char.isdigit() for char in new_code.code)
        assert new_code.expiry_date > datetime.now()

    def test_valid_activation_code(self, user_activation_code):
        assert user_activation_code.is_code_valid(input_code="1234")

    def test_not_valid_activation_code(self, user_activation_code):
        assert not user_activation_code.is_code_valid(input_code="wrong")

    def test_expired_activation_code(self, user_activation_code):
        user_activation_code.expiry_date = datetime.now() - timedelta(minutes=1)
        assert not user_activation_code.is_code_valid(input_code="1234")
