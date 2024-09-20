import asyncio
import logging
import sys

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text

logger = logging.getLogger(__name__)


if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async_engine = create_async_engine(
    url="postgresql+psycopg://postgres:postgres@localhost:5432/alch",
    # url="postgresql+psycopg://pguser:000000@localhost:5432/mydb",
    echo=True,
    # pool_size=5,
    # max_overflow=10
)

session_factory = async_sessionmaker(async_engine)
Base = declarative_base()
