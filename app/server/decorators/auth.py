from functools import wraps

from flask import g, session

from app.db.models import User
from app.server.enums import StatusCodes
from app.server.formatters.errors import format_status_code


def set_current_user():
    if session.get("uid"):
        g.current_user = User.lookup_by_id(session["uid"])
    else:
        g.current_user = None


def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if not g.current_user:
            return format_status_code(StatusCodes.HTTP_401_UNAUTHORIZED)

        return route(*args, **kwargs)

    return wrapper
