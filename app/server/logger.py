import json
import logging
import sys
from collections.abc import Mapping
from itertools import chain

from app.server.request_ids import get_request_id

DEFAULT_LOGGER_NAME = __name__
LOGGED_FIELDS = {"file": "%(pathname)s:%(lineno)d"}


class JsonLogFormatter(logging.Formatter):
    base_fields = {
        "level": "%(levelname)s",
        "logger": "%(name)s",
        "process": "%(process)d",
        # exception_trace, if present
        # stacktrace, if present
        # request_id, if available
        # timestamp
        # message
    }

    def __init__(self, *_args, extra_fields=None):
        # *args is needed because alembic passes in parameters automatically
        super().__init__()
        self.extra_fields = extra_fields or {}

    def format(self, record):
        if isinstance(record.args, Mapping):
            # gunicorn `atoms` are passed in as record.args
            record_dict = {**record.__dict__, **record.args}
        else:
            record_dict = record.__dict__

        kv_pairs = chain(
            self.base_fields.items(),
            self.extra_fields.items(),
            (record_dict.get("extra") or {}).items(),
        )
        log = {k: str(v) % record_dict for k, v in kv_pairs}

        if record.exc_info:
            log["exception_trace"] = self.formatException(record.exc_info)
        if record.stack_info:
            log["stacktrace"] = self.formatStack(record.stack_info)

        request_id = record_dict.get("request_id") or get_request_id()
        if request_id:
            log["request_id"] = request_id

        log["timestamp"] = self.formatTime(record, datefmt="%Y-%m-%d %H:%M:%S.{:03.0f} %z").format(
            record.msecs
        )
        log["message"] = record.getMessage()
        return json.dumps(log)


class CustomLogger(logging.Logger):
    def makeRecord(  # pylint: disable=too-many-arguments
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ):
        """
        Nest `extra` 1 level deeper so all the extras are easy to find and format
        """
        extra = {
            "extra": extra,
            # could splat extra here to make available in log strings
        }
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)


# this applies to both the api and flask loggers
logging.setLoggerClass(CustomLogger)

_logger = logging.getLogger(DEFAULT_LOGGER_NAME)
_logger.setLevel("INFO")
_logger.addHandler(logging.StreamHandler(sys.stdout))
_logger.handlers[0].setFormatter(JsonLogFormatter(extra_fields=LOGGED_FIELDS))


def get_logger():
    return logging.getLogger(DEFAULT_LOGGER_NAME)


def setup_flask_logger(app):
    # Setup flask logging (uncaught exceptions, etc.)
    app.logger.setLevel("INFO")
    # app.logger.handlers[0].setFormatter(JsonLogFormatter(extra_fields=LOGGED_FIELDS))
