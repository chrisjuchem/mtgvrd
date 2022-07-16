from flask import g
from uuid import uuid4

REQUEST_ID_HEADER = "X-Request-Id"


def get_request_id():
    try:
        if "request_id" not in g:
            g.request_id = str(uuid4())
    except RuntimeError:  # outside a request
        return None
    return g.request_id
