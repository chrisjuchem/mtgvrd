from functools import wraps

import trafaret as t
from flask import request

from app.server.enums import ParamSources, StatusCodes
from app.server.logger import get_logger


def validate(source, trafaret):
    """
    Usage:

    @blueprint.route(...)
    @validate(ParamSources.JSON, x_trafaret)
    def my_route(validated_data):
        ...
    """

    def route_wrapper(route):
        @wraps(route)
        def validation_wrapper(*args, **kwargs):
            if source == ParamSources.QUERY_ARGS:
                params = request.args
            else:
                params = request.json

            if source == ParamSources.JSON and request.json is None:
                return (
                    {"error": "No JSON data. Perhaps you did not set Content-Type."},
                    StatusCodes.HTTP_400_BAD_REQUEST,
                )

            try:
                validated = trafaret.check(params)
            except t.DataError as exc:
                return {"errors": exc.as_dict()}, StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY
            except UnicodeError as exc:
                get_logger().warning("UnicodeError during traf decode. Message: {}".format(exc))
                return {"error": "Invalid request data"}, StatusCodes.HTTP_400_BAD_REQUEST

            # passes the validated data in directly as an arg, the route function must accept it
            return route(validated, *args, **kwargs)

        return validation_wrapper

    return route_wrapper
