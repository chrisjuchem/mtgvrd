from contextlib import contextmanager

from flask_sqlalchemy_session import current_session, flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.server.config import config


def get_database_url():
    url = "postgresql://{}:{}@{}:{}/{}".format(
        config["DB_USER"],
        config["DB_PASSWORD"],
        config["DB_HOST"],
        config["DB_PORT"],
        config["DB_NAME"],
    )
    return url


def build_engine(**kwargs):
    return create_engine(get_database_url(), echo=True, **kwargs)


engine = build_engine()
session_factory = sessionmaker(bind=engine)


def setup_flask_db_session(app):
    flask_scoped_session(session_factory, app)


@contextmanager
def ensure_session(session=None):
    # This is the primary way to get access to a session
    if session:
        yield session
    elif current_session:
        yield current_session
    else:
        new_session = session_factory()
        try:
            yield new_session
        finally:
            new_session.close()
