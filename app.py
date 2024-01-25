import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv
from handlers.user_private import user_private_router
from common.bot_cmds_list import private
from handlers.user_proup import user_group_router

# default file name for find '.env'
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


dp.include_router(user_group_router)
dp.include_router(user_private_router)

ALLOWED_UPDATES = ['message, edited_message']


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=private,
        scope=BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())
