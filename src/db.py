from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
import asyncio
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL, echo=True)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class BaseOrm(DeclarativeBase):
    pass

