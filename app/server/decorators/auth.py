from functools import wraps

from flask import session

from app.db.models import User
from app.server.enums import StatusCodes
from app.server.formatters.errors import format_status_code


def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        user = None
        if session.get("uid"):
            user = User.lookup_by_id(session["uid"])

        if not user:
            return format_status_code(StatusCodes.HTTP_401_UNAUTHORIZED)

        return route(*args, current_user=user, **kwargs)

    return wrapper
