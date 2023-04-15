import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://{username}:{password}@{host}:{port}/{database}")

async_engine = create_async_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=async_engine)

Base = declarative_base()


async def get_db() -> Session:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
