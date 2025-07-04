import sys
import asyncio
from logging.config import fileConfig
from os.path import dirname, abspath

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from alembic import context

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from src.services.db_client import Base, DATABASE_URL

# Проверка строки подключения
print(f"Using DATABASE_URL: {DATABASE_URL}")  # Для отладки

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DATABASE_URL)
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Асинхронное выполнение миграций."""
    # Устанавливаем уровень логирования для отладки
    #logging.basicConfig(level=logging.INFO)

    engine = create_async_engine(
        DATABASE_URL,
        #echo=True,  # Включаем вывод SQL-запросов
        poolclass=pool.NullPool,
    )

    async with engine.connect() as conn:
        await conn.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )
        async with conn.begin():
            await conn.run_sync(lambda sync_conn: context.run_migrations())


def run_migrations_online():
    """Запуск асинхронных миграций в основном потоке."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()