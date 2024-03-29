from functools import cached_property
from urllib.parse import urljoin

import requests
from authlib.common.errors import AuthlibBaseError
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, g, redirect, request, session
from flask_sqlalchemy_session import current_session
from sqlalchemy import func
from werkzeug.exceptions import BadRequestKeyError

from app.db.models.user import User
from app.server.config import config
from app.server.decorators.validation import validate
from app.server.enums import ParamSources, StatusCodes
from app.server.formatters.errors import format_status_code
from app.server.logger import get_logger
from app.server.trafarets.login import callback_trafaret, redirect_trafaret


class ClientRegistry:
    """
    Wrapper class to delay client setup until first access
    so that env vars can be overwritten successfully in tests
    """

    def __init__(self):
        self.clients = OAuth()
        self.setup = False

    def setup_clients(self):
        self.clients.register(
            name="discord",  # used to reference the client in registry
            client_id=config["DISCORD_CLIENT_ID"],
            client_secret=config["DISCORD_CLIENT_SECRET"],
            # server_metadata_url=config['OIDC_DISCOVERY_URL'],
            authorize_url=config["DISCORD_AUTHORIZE_URL"],
            authorize_params=None,
            access_token_url=config["DISCORD_ACCESS_TOKEN_URL"],
            access_token_params=None,
            client_kwargs={"scope": "identify"},
        )
        self.setup = True

    def create_client(self, provider):
        if not self.setup:
            self.setup_clients()
        return self.clients.create_client(provider)

    @cached_property
    def user_info_endpoints(self):
        return {"discord": config["DISCORD_USER_INFO_URL"]}


oauth_clients = ClientRegistry()


def setup_login(app):
    oauth_clients.clients.init_app(app)


login_routes = Blueprint("Login", __name__)


@login_routes.route("/<string:provider>/redirect")
@validate(ParamSources.QUERY_ARGS, redirect_trafaret)
def oauth_redirect(request_data, provider):
    oauth_client = oauth_clients.create_client(provider)
    if not oauth_client:
        return format_status_code(StatusCodes.HTTP_404_NOT_FOUND)

    back_to = request_data.get("back_to")
    if back_to:
        session["back_to"] = back_to

    redirect_uri = urljoin(request.host_url, f"/login/{provider}/callback")
    return oauth_client.authorize_redirect(redirect_uri)


@login_routes.route("/<string:provider>/callback")
@validate(ParamSources.QUERY_ARGS, callback_trafaret)
def oauth_callback(_request_data, provider):
    oauth_client = oauth_clients.create_client(provider)
    if not oauth_client:
        return format_status_code(StatusCodes.HTTP_404_NOT_FOUND)

    back_to = session.pop("back_to", "/")
    try:
        token_response = oauth_client.authorize_access_token()
    except (AuthlibBaseError, BadRequestKeyError) as exc:
        get_logger().warning("Error during OAuth flow: %s", exc)
        return redirect("/login/error")

    user_info = requests.get(
        oauth_clients.user_info_endpoints[provider],
        headers={"Authorization": f"Bearer {token_response['access_token']}"},
    ).json()

    user = User.lookup_by_id(user_info["id"], provider)
    if not user:
        user = User.from_dict(
            {
                f"{provider}_id": user_info["id"],
                "username": user_info["username"],
            }
        )
        current_session.add(user)
    user.last_login = func.now()

    current_session.commit()

    session["uid"] = user.id

    return redirect(back_to)


@login_routes.route("/logout")
@validate(ParamSources.QUERY_ARGS, redirect_trafaret)
def logout(validated_data):
    session.pop("uid", None)
    return redirect(validated_data.get("back_to", "/"))


@login_routes.route("/check")
def check_auth():
    if not g.current_user:
        return {"logged_in": False}
    return {
        "logged_in": True,
        "uid": g.current_user.id,
        "username": g.current_user.username,
    }
