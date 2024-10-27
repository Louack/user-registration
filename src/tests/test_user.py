from pytest import fixture

from src.auth.core.domain.user import User


@fixture()
def user():
    return User(email="test@test.com", password="1234")


class TestUser:
    def test_default_not_active_user(self, user):
        assert not user.is_active
