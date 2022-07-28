class ParamSources:
    JSON = "json"
    QUERY_ARGS = "query_args"

    ALL = [JSON, QUERY_ARGS]


class StatusCodes:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_409_CONFLICT = 409
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_500_INTERNAL_SERVER_ERROR = 500