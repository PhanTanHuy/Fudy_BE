import os

from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://fudy_dev:change_me@localhost:5432/fudy_dev",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
