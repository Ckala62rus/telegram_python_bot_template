import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
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


@dp.message(Command('phone'))
async def start_command(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(
            chat_id=message.chat.id,
            text='Отправьте свой номер телефона',
            reply_markup=types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                selective=True,
                one_time_keyboard=True,
                keyboard=[
                    [
                        types.KeyboardButton(
                            text='Отправить номер телефона',
                            request_contact=True
                        )
                    ]
                ],
            ),
        )


# @dp.message(content_types=types.ContentType.CONTACT)
# async def process_contact(message: Message):
#     async with aiosession.get(f" https://api.telegram.org/bot{}/getChat?chat_id={message.from_user.id} ") as resp:
#     result = await resp.json()
#     print(result["result"]["phone_number"])


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=private,
        scope=BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


# asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())
