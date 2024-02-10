import asyncio
import sys

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text


if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async_engine = create_async_engine(
    url="postgresql+psycopg://pguser:000000@localhost:5432/alch",
    # url="postgresql+psycopg://pguser:000000@localhost:5432/mydb",
    echo=True,
    # pool_size=5,
    # max_overflow=10
)

session_factory = async_sessionmaker(async_engine)
Base = declarative_base()


# async def get():
#     # with async_engine.connect() as conn:
#     #     res = conn.execute(text("select * from user"))
#     #     result = res.all()
#     #     print(result)
#     #     # a = select(worker)
#
#     async with session_factory() as session:
#         session.add("")
#         await session.commit()
#
#
# asyncio.run(get())
