import os

import pytest
from sqlalchemy import func

from app.db.connection import ensure_session
from app.db.models import User
from app.server.app import app

if not os.environ.get("TEST_ENVIRONMENT"):
    raise RuntimeError(
        "Environment error."
        " -- Some tests require the use of a database. This check ensures that you "
        "are not connecting to your local database, which could result in a loss "
        "of data. Use ./run_pytest.sh to run tests with a test database "
        "(this script passes through arguments)."
    )


DISCORD_AUTHORIZE_URL = "http://mock_discord_auth_url"
DISCORD_ACCESS_TOKEN_URL = "http://mock_discord_token_url"
DISCORD_USER_INFO_URL = "http://mock_discord_user_url"

MOCK_URLS = {
    "discord": {
        "authorize": DISCORD_AUTHORIZE_URL,
        "token": DISCORD_ACCESS_TOKEN_URL,
        "user_info": DISCORD_USER_INFO_URL,
    }
}


# pylint: disable=redefined-outer-name
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Sets the required env vars for tests"""
    monkeypatch.setenv("DISCORD_AUTHORIZE_URL", DISCORD_AUTHORIZE_URL)
    monkeypatch.setenv("DISCORD_ACCESS_TOKEN_URL", DISCORD_ACCESS_TOKEN_URL)
    monkeypatch.setenv("DISCORD_USER_INFO_URL", DISCORD_USER_INFO_URL)


@pytest.fixture
def db_session():
    with ensure_session() as ses:
        yield ses


@pytest.fixture
def user_factory(db_session):
    def factory(fields: dict):
        fields.setdefault("last_login", func.now())
        fields.setdefault("discord_id", "1234")

        usr = User.from_dict(fields)
        db_session.add(usr)
        db_session.commit()
        return usr

    return factory


@pytest.fixture()
def client_factory():
    def factory():
        with app.test_client() as client:
            return client

    return factory


@pytest.fixture
def no_session_client(client_factory):
    yield client_factory()


@pytest.fixture
def session_user(user_factory):
    return user_factory({"username": "session_user"})


@pytest.fixture
def user_client_factory(client_factory):
    def factory(user):
        client = client_factory()
        with client.session_transaction() as session:
            session["uid"] = user.id
        return client

    return factory


@pytest.fixture
def session_client(user_client_factory, session_user):
    return user_client_factory(session_user)
