import os
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.domain.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://{username}:{password}@{host}:{port}/{database}")

engine = create_async_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

async_session = sessionmaker(engine, expire_on_commit=False, class_='AsyncSession')

@asynccontextmanager
async def get_db():
    async with async_session() as session:
        yield session
