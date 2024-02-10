from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query_user import get_user_by_telegram_id, add_user
from filters.chat_types import ChatTypeFilter
from kbds import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_command(message: types.Message, db_session: AsyncSession):
    # await message.answer(text="This command '/start'")
    user = await get_user_by_telegram_id(db_session, message.from_user.id)

    if user is None:
        await add_user(db_session, {
            "username": message.from_user.username,
            "telegram_id": message.from_user.id,
        })

    await message.answer(
        text="This command '/start'",
        reply_markup=reply.start_kb
    )


@user_private_router.message(Command('menu'))
async def start_command(message: types.Message, db_session: AsyncSession):
    try:
        # user = User(
        #     username=message.from_user.username,
        # )
        # db_session.add(user)
        # await db_session.commit()
        # query = select(User)
        # result = await db_session.execute(query)
        # res = result.scalars().all()
        print("hello! menu command")
    except Exception as ex:
        print(ex)
    await message.answer(text="Вот меню")


@user_private_router.message(Command('about'))
async def start_command(message: types.Message):
    await message.answer(text="О нас")


@user_private_router.message(Command('payment'))
async def start_command(message: types.Message):
    await message.answer(text="Оплата")


@user_private_router.message(Command('shipping'))
async def start_command(message: types.Message):
    await message.answer(text="Доставка")


# "^([0-9]{2,4})@([a-zA-Z]{0,5})$" => 1234@test
@user_private_router.message(F.text.regexp("^([0-9]{2,4})@([a-zA-Z]{0,5})$"))
async def start_command(message: types.Message):
    await message.answer(text=message.text)


@user_private_router.message(Command('phone'))
async def start_command(message: types.Message):
    await message.answer(
        text="Отправьте свой номер телефона",
        reply_markup=reply.phone_kb
    )


@user_private_router.message(F.contact)
async def start_command(message: types.Message):
    await message.answer(
        text=f"Вот твой номер: {message.contact.phone_number}")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def start_command(message: types.Message):
    await message.answer(text="Ваша локация")
    await message.answer(str(message.location))

# @user_private_router.message(F.text)
# async def start_command(message: types.Message):
#     await message.answer(text="Это магический фильтр")


# @user_private_router.message()
# async def echo(message: types.Message):
#     await message.answer(message.text)
