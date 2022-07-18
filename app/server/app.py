from app.server.logger import get_logger

from flask import Flask, send_from_directory

from app.server.app_config import app_config
from app.db.connection import setup_flask_db_session
from app.server.logger import setup_flask_logger

from app.server.request_ids import get_request_id, REQUEST_ID_HEADER


app = Flask(__name__, static_folder='../client/build')
app.config.from_object(app_config)


setup_flask_logger(app)
setup_flask_db_session(app)


@app.route("/ping")
def ping():
    get_logger().info("PINGED", extra={'dd':33})
    return '"pong"'


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "":  # and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.after_request
def add_response_headers(response):
    # Add some security headers to all responses
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=16070400; includeSubDomains"
    response.headers["Expect-CT"] = "max-age=86400, enforce"

    response.headers[REQUEST_ID_HEADER] = get_request_id()

    return response
