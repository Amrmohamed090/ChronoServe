# app/config.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://chronouser:chronopass@db/chronoserve"
)
