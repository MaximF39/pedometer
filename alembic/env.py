import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# target_metadata = None
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
# sys.path.append(parent_dir)
import sys

sys.path.append(os.getcwd())
from src.core.models import Base

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """
    Run versions in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run versions in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_config = config.get_section(config.config_ini_section)

    alembic_config["sqlalchemy.url"] = "{drivername}://{username}:{password}@{host}:{port}/{database}".format(
        drivername="postgresql",
        username="postgres",
        password="postgres",
        host="postgres",
        port=5432,
        database="postgres",
    )
    print(alembic_config["sqlalchemy.url"])

    engine = engine_from_config(alembic_config)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
