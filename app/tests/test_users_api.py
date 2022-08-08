from app.tests.helpers import TestBaseEphemeral


class TestUsersApi(TestBaseEphemeral):
    def test_get_self_no_login(self, no_session_client):
        resp = no_session_client.get("/api/users/me")
        assert resp.status_code == 401
        assert resp.json == {"error": "Login required"}

    def test_get_self(self, session_client, session_user):
        resp = session_client.get("/api/users/me")
        assert resp.status_code == 200
        assert resp.json == {
            "id": session_user.id,
            "username": session_user.username,
        }
