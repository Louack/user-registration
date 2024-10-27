from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from src.builders.use_cases_builders import (
    get_user_activation_use_case,
    get_user_auth_use_case,
    get_user_registration_use_case,
)
from src.main import app

mock_use_case_fixture = MagicMock()


def override_get_use_case():
    return mock_use_case_fixture


app.dependency_overrides[get_user_registration_use_case] = override_get_use_case
app.dependency_overrides[get_user_auth_use_case] = override_get_use_case
app.dependency_overrides[get_user_activation_use_case] = override_get_use_case


@pytest.fixture
def mock_registration_use_case():
    return mock_use_case_fixture


@pytest.fixture
def mock_verification_use_case():
    return mock_use_case_fixture


@pytest.fixture
def mock_activation_use_case():
    return mock_use_case_fixture


@pytest.fixture()
def client():
    return TestClient(app)
