from aiogram import types, Bot
from aiogram.filters import Filter
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_user import get_admins_user


# filter for check private of public chat
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admins_list


class IsAdminFromDatabase(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            message: types.Message,
            bot: Bot,
            db_session: AsyncSession
    ):

        is_exist = message.from_user.id in bot.my_admins_list

        if is_exist is False:
            users = await get_admins_user(db_session)

            for user in users:
                bot.my_admins_list.append(user.telegram_id)

            return message.from_user.id in bot.my_admins_list

        return is_exist
