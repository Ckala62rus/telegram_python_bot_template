from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

from database.orm_query_command import add_user_command
from database.orm_query_user import get_user_by_telegram_id


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker) -> None:
        self.db_session = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.db_session() as session:
            data['db_session'] = session
            return await handler(event, data)


class SaveInputCommandMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        session = data['db_session']
        text = event.message.text
        telegram_user_id = event.message.chat.id

        user = await get_user_by_telegram_id(session, telegram_user_id)

        if user is not None:
            await add_user_command(session, {
                "command": text,
                "user_id": user.id,
            })

            await session.commit()

        return await handler(event, data)
