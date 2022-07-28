from sqlalchemy import inspect
from werkzeug.routing import UUIDConverter, ValidationError

from app.db.models import BaseModel


def setup_routing(app):
    app.url_map.strict_slashes = False

    app.url_map.converters["record"] = RecordConverter


class RecordConverter(UUIDConverter):
    """Url param converter for models with UUID PKs"""

    def __init__(self, *args, **kwargs):
        self.model_class = BaseModel.registry._class_registry[  # pylint: disable=no-member
            kwargs.pop("model")
        ]
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        record = self.model_class.lookup_by_id(value)
        if not record:
            raise ValidationError
        return record

    def to_url(self, value):
        primary_key = inspect(self.model_class).primary_key
        return getattr(value, primary_key[0].name)
