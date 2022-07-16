import os

from app.server.request_ids import REQUEST_ID_HEADER

accesslog = "-"
# default: '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
access_log_format = (
    "%(t)s "      # timestamp
    '"%(r)s" '    # request string
    "%(s)s "      # status code
    "%(M)dms "    # response time
    "%(h)s "      # remote address
    f"%({{{REQUEST_ID_HEADER}}}o)s "  # request id
    "ref:%(f)s "  # referrer
    "%(a)s"       # user agent
)
loglevel = "info"

bind = "0.0.0.0:{}".format(os.environ.get("APP_PORT", 5000))
workers = int(os.environ["GUNICORN_WORKERS"])
threads = int(os.environ["GUNICORN_THREADS"])



# logger_class = ExtendedGunicornLogger
#
#
#
# import sys
# from gunicorn.glogging import Logger as BaseGunicornLogger
#
# from api.src.logging.json_log_formatter import JsonLogFormatter, USE_JSON_LOGS
# from api.src.logging.request_ids import REQUEST_ID_HEADER
#
#
# class ExtendedGunicornLogger(BaseGunicornLogger):
#     def atoms(self, resp, req, environ, request_time):
#         """
#         Adds custom fields to access log atoms formatting
#         """
#         atoms_dict = super().atoms(resp, req, environ, request_time)
#
#         # get_request_id() will not work here because this is handled outside
#         # of the flask request context
#         for header, val in resp.headers:
#             # wsgi response headers are a list of tuples, not a dict
#             if header == REQUEST_ID_HEADER:
#                 atoms_dict["request_id"] = val
#                 break
#
#         return atoms_dict
#
#     def setup(self, cfg):
#         super().setup(cfg)
#         if USE_JSON_LOGS:
#             self._set_handler(
#                 self.error_log,
#                 cfg.errorlog,
#                 JsonLogFormatter(),
#             )
#             self._set_handler(
#                 self.access_log,
#                 cfg.accesslog,
#                 JsonLogFormatter(
#                     extra_fields={
#                         # The values for these identifiers is set by the `atoms` function
#                         "remote_address": "%(h)s",
#                         "request": "%(r)s",
#                         "request_method": "%(m)s",
#                         "path": "%(U)s",
#                         "referrer": "%(f)s",
#                         "query_string": "%(q)s",
#                         "status_code": "%(s)s",
#                         "user_agent": "%(a)s",
#                         "request_time": "%(L)s",
#                     }
#                 ),
#                 sys.stdout,
#             )
