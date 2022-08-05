from datetime import datetime

import pytest
from flask import session

from app.db.connection import ensure_session
from app.db.models import User
from app.tests.helpers import TestBaseEphemeral


class TestSomething(TestBaseEphemeral):  # todo enforce this inheritece
    def test_true(self):
        assert True

    def test_false(self):
        assert not False

    def test_users(self):
        assert User.query().count() == 0
        u = User(username="test1", discord_id="1", last_login=datetime.now())
        with ensure_session() as s:
            s.add(u)
            s.commit()
        assert User.query().count() == 1

    @pytest.mark.parametrize(["provider"], [["discord"]])
    def test_login(self, client, provider):
        assert User.query().count() == 0

        resp = client.get(f"login/{provider}/redirect")

        assert session == {}

        assert resp.status_code == 302

        resp = client.get(f"login/{provider}/callback?code=1234&state=5678")
