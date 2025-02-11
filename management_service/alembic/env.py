import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

# 1) This loads your Pydantic config
from config import settings  

# 2) Import your Base metadata from models (so Alembic sees your tables)
from models import Base

fileConfig(context.config.config_file_name)
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    # return the same DB URL your main code uses
    return settings.DATABASE_URL

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


def main():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()

if __name__ == "__main__":
    main()
