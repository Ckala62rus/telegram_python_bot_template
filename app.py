import asyncio
import logging.config
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv
from database.db import session_factory
from common.bot_cmds_list import private
from handlers.user_private import user_private_router
from handlers.user_proup import user_group_router
from handlers.admin_private import admin_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sheduler import scheduler_tasks

from utils.logger_project import logging_config

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())
from middleware.db_middleware import DatabaseSessionMiddleware, \
    SaveInputCommandMiddleware


# default file name for find '.env'
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []
dp = Dispatcher()

dp.include_router(user_group_router)
dp.include_router(user_private_router)
dp.include_router(admin_router)

ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']


async def main():
    logger.debug('start application')
    # cron scheduler apscheduler
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.add_job(scheduler_tasks.every_minutes, trigger='interval', seconds=60, kwargs={'bot': bot})
    # scheduler.start()

    # init database session via middleware
    logger.debug('init middlewares')
    dp.update.middleware(DatabaseSessionMiddleware(session_pool=session_factory))
    dp.update.middleware(SaveInputCommandMiddleware())
    logger.debug('end init middlewares')

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=private,
        scope=BotCommandScopeAllPrivateChats()
    )
    logger.debug('start polling')
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
