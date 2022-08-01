from .app import app_routes
from .draft import draft_routes
from .login import login_routes
from .user import user_routes

blueprints = [
    (app_routes, ""),
    (login_routes, "/login"),
    (user_routes, "/api/users"),
    (draft_routes, "/api/drafts"),
]
