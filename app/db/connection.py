from contextlib import contextmanager
from os import environ
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_sqlalchemy_session import current_session, flask_scoped_session


def get_database_url():
    url = "postgresql://{}:{}@{}:{}/{}".format(
        environ.get("DB_USER", "local_db_user"),
        environ.get("DB_PASSWORD", "blacklotus"),
        environ.get("DB_HOST", "0.0.0.0"),
        environ.get("DB_PORT", "5432"),
        environ.get("DB_NAME", "mtgvrd"),
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
        s = session_factory()
        try:
            yield s
        finally:
            s.close()
