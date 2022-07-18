from os import getcwd
import sys
import logging

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Set up path to app
sys.path.insert(0, getcwd())

from app.db.connection import get_database_url
# import Base from the module to make sure we pick up models from other files too
from app.db.models import Base


# support migration auto-generation
target_metadata = Base.metadata


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Optional features
context_opts = {
    # migration options
    "transaction_per_migration": True,
    # autogenerate options
    "compare_type": True,
    "compare_server_default": True,
    # "include_object": some_func,
}



def run_migrations_offline():
    """Run versions in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **context_opts,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run versions in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        # config.get_section(config.config_ini_section),
        {"sqlalchemy.url": get_database_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            **context_opts,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


try:
    run_migrations()
except Exception:
    logging.exception("Exception while running versions")
    exit(1)