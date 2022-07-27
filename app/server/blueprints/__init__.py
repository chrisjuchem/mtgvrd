from .app import app_routes
from .draft import draft_routes

blueprints = [
    (app_routes, ""),
    (draft_routes, "/api/drafts"),
]
