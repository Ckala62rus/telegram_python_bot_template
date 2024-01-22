from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(text="This command '/start'")


@user_private_router.message(Command('menu'))
async def start_command(message: types.Message):
    await message.answer(text="Вот меню")


@user_private_router.message(Command('about'))
async def start_command(message: types.Message):
    await message.answer(text="О нас")


@user_private_router.message()
async def echo(message: types.Message):
    if message.contact is not None:
        await message.answer(message.contact.phone_number)
    else:
        await message.answer(message.text)

