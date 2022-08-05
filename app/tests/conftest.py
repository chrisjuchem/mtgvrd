import os

import pytest

from app.db.connection import ensure_session
from app.server.app import app

if not os.environ.get("TEST_ENVIRONMENT"):
    raise RuntimeError(
        "Environment error."
        " -- Some tests require the use of a database. This check ensures that you "
        "are not connecting to your local database, which could result in a loss "
        "of data. Use ./run_pytest.sh to run tests with a test database "
        "(this script passes through arguments)."
    )


@pytest.fixture
def db_session():
    with ensure_session() as ses:
        yield ses


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Sets the required env vars for tests"""
    monkeypatch.setenv("SOME_VAR", "MOCK_VALUE")


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
