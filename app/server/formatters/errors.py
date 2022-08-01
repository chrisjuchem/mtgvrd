from app.server.enums import StatusCodes


def format_status_code(code):
    """Provide a standard response for generic error codes"""
    if code == StatusCodes.HTTP_204_NO_CONTENT:
        return "", code
    if code == StatusCodes.HTTP_401_UNAUTHORIZED:
        return {"error": "Login required"}, code
    if code == StatusCodes.HTTP_404_NOT_FOUND:
        return {"error": "Not found"}, code

    return {"error": code}, code
