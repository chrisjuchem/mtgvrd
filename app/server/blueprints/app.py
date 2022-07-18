from flask import Blueprint, send_from_directory

from app.server.logger import get_logger


app_routes = Blueprint("App", __name__, static_folder='../../client/build')


@app_routes.route("/ping")
def ping():
    return '"pong"'


# Serve React App
@app_routes.route('/', defaults={'path': ''})
@app_routes.route('/<path:path>')
def serve(path):
    if path:
        asset_response = send_from_directory(app_routes.static_folder, path)
        if asset_response.status_code != 404:
            return asset_response
    # let the frontend handle loading the right page
    get_logger().warning("Missing asset - returning index.html", extra={"path": path})
    return send_from_directory(app_routes.static_folder, 'index.html')
