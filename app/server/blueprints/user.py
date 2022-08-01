from flask import Blueprint

from app.server.decorators.auth import login_required
from app.server.decorators.validation import validate
from app.server.enums import ParamSources
from app.server.formatters.user import format_user
from app.server.trafarets.user import user_update_trafaret

user_routes = Blueprint("User", __name__)


@user_routes.route("/me")
@login_required
def self_info(current_user):
    return format_user(current_user)


@user_routes.route("/me", methods=["PATCH"])
@login_required
@validate(ParamSources.JSON, user_update_trafaret)
def update_self(validated_data, current_user):
    current_user.update_from_dict(validated_data)
    current_user.save()

    return format_user(current_user)


@user_routes.route("/<record(model=User):user>")
def get_user(user):
    return format_user(user)
