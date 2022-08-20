from urllib.parse import parse_qs, urlsplit

import pytest
import responses

from app.db.models import User
from app.tests.conftest import MOCK_URLS
from app.tests.helpers import ABOUT_NOW, TestBaseEphemeral


class TestLogin(TestBaseEphemeral):  # todo enforce this inheritece
    def create_login_mocks(self, code, redirect_uri, provider_id, username, urls):
        token = "tokenABCD"

        responses.add(
            responses.POST,
            urls["token"],
            match=[
                responses.matchers.urlencoded_params_matcher(
                    {
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": redirect_uri,
                        # I'm 90 % sure there should be a client id and secret here
                    }
                )
            ],
            json={"access_token": token},
        )
        responses.add(
            responses.GET,
            urls["user_info"],
            json={"id": provider_id, "username": username},
        )

        return token

    @responses.activate
    @pytest.mark.parametrize(["provider"], [["discord"]])
    def test_login(self, no_session_client, provider):
        assert User.query().count() == 0

        assert not no_session_client.get("login/check").json["logged_in"]

        back_to = "back_to_path"
        resp = no_session_client.get(f"login/{provider}/redirect?back_to={back_to}")

        assert resp.status_code == 302
        auth_redirect = resp.headers["Location"]
        assert MOCK_URLS[provider]["authorize"] in auth_redirect
        auth_redirect_qs = parse_qs(urlsplit(auth_redirect).query)

        code = "1a2b3c4d5e"
        state = auth_redirect_qs["state"][0]
        provider_id = "foo"
        username = "test_user"

        self.create_login_mocks(
            code=code,
            redirect_uri=auth_redirect_qs["redirect_uri"][0],
            username=username,
            provider_id=provider_id,
            urls=MOCK_URLS[provider],
        )

        resp = no_session_client.get(f"login/{provider}/callback?code={code}&state={state}")

        assert resp.status_code == 302
        assert resp.headers["Location"] == back_to

        assert User.query().count() == 1
        user = User.query().first()
        assert user.username == username
        assert getattr(user, f"{provider}_id") == provider_id
        assert user.last_login == ABOUT_NOW

        assert no_session_client.get("login/check").json["logged_in"]
        assert no_session_client.get("login/check").json["uid"] == user.id
        assert no_session_client.get("login/check").json["username"] == username

    @responses.activate
    @pytest.mark.parametrize(["provider"], [["discord"]])
    def test_login_preexisting(self, no_session_client, provider, user_factory):
        provider_id = "foo"
        username = "existing_username"

        existing_user = user_factory(
            {
                f"{provider}_id": provider_id,
                "username": username,
            }
        )
        assert User.query().count() == 1
        previous_login = existing_user.last_login

        assert not no_session_client.get("login/check").json["logged_in"]

        back_to = "back_to_path"
        resp = no_session_client.get(f"login/{provider}/redirect?back_to={back_to}")

        assert resp.status_code == 302
        auth_redirect = resp.headers["Location"]
        assert MOCK_URLS[provider]["authorize"] in auth_redirect
        auth_redirect_qs = parse_qs(urlsplit(auth_redirect).query)

        code = "1a2b3c4d5e"
        state = auth_redirect_qs["state"][0]

        self.create_login_mocks(
            code=code,
            redirect_uri=auth_redirect_qs["redirect_uri"][0],
            provider_id=provider_id,
            username=username,
            urls=MOCK_URLS[provider],
        )

        resp = no_session_client.get(f"login/{provider}/callback?code={code}&state={state}")

        assert resp.status_code == 302
        assert resp.headers["Location"] == back_to

        assert User.query().count() == 1
        user = User.lookup_by_id(existing_user.id)
        assert user.username == username
        assert getattr(user, f"{provider}_id") == provider_id
        assert user.last_login == ABOUT_NOW
        assert user.last_login != previous_login

        assert no_session_client.get("login/check").json["logged_in"]
        assert no_session_client.get("login/check").json["uid"] == existing_user.id
        assert no_session_client.get("login/check").json["username"] == username


# TODO test user routes
