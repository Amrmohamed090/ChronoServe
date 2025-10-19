# app/db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Base class for models
Base = declarative_base()

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)



