from flask import Flask

from app.db.connection import setup_flask_db_session
from app.server.blueprints import blueprints
from app.server.blueprints.login import setup_login
from app.server.config import app_config
from app.server.decorators.auth import set_current_user
from app.server.logger import setup_flask_logger
from app.server.request_ids import REQUEST_ID_HEADER, get_request_id
from app.server.routing import setup_routing

app = Flask(__name__, static_folder=None)
app.config.from_object(app_config)

setup_flask_logger(app)
setup_flask_db_session(app)
setup_routing(app)
setup_login(app)

for blueprint, prefix in blueprints:
    app.register_blueprint(blueprint, url_prefix=prefix)


app.before_request(set_current_user)


@app.after_request
def add_response_headers(response):
    # Add some security headers to all responses
    response.headers["Strict-Transport-Security"] = "max-age=16070400; includeSubDomains"
    response.headers["Expect-CT"] = "max-age=86400, enforce"

    response.headers[REQUEST_ID_HEADER] = get_request_id()

    return response
