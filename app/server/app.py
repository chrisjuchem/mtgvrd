from app.server.logger import get_logger

from flask import Flask

from app.server.app_config import app_config
from app.db.connection import setup_flask_db_session
from app.server.logger import setup_flask_logger

from app.server.request_ids import get_request_id, REQUEST_ID_HEADER


app = Flask(__name__)
app.config.from_object(app_config)


setup_flask_logger(app)
setup_flask_db_session(app)


@app.route("/ping")
def ping():
    get_logger().info("PINGED", extra={'dd':33})
    return '"pong"'


@app.after_request
def add_response_headers(response):
    # Add some security headers to all responses
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=16070400; includeSubDomains"
    response.headers["Expect-CT"] = "max-age=86400, enforce"

    response.headers[REQUEST_ID_HEADER] = get_request_id()

    return response
