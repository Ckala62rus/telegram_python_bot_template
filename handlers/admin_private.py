import logging

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_user import get_user_by_phone_number, \
    set_admin_for_user
from filters.chat_types import ChatTypeFilter, IsAdmin, IsAdminFromDatabase
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdminFromDatabase())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Я так, просто посмотреть зашел",
    "Назначить админа",
    placeholder="Выберите действие",
    sizes=(2, 1, 1)
)

CANCEL_BT = get_keyboard(
    "отмена",
)


@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Я так, просто посмотреть зашел")
async def starring_at_product(message: types.Message):
    logger.debug("DEBUG показ инлайн сообщения с кнопками")
    logger.info("INFO показ инлайн сообщения с кнопками")
    logger.warning("WARNING показ инлайн сообщения с кнопками")
    logger.error("ERROR показ инлайн сообщения с кнопками")
    logger.critical("CRITICAL показ инлайн сообщения с кнопками")

    # markup = InlineKeyboardMarkup()
    # markup.add(
    #     InlineKeyboardButton
    #     (
    #         'Инлайн кнопка', reply_markup=get_callback_btns(btns={
    #             "Удалить": f"delete_{1}",
    #             "Измменить": f"delete_{2}",
    #         })
    #     )
    # )

    await message.answer("какой то товар", reply_markup=get_callback_btns(btns={
        "Удалить": f"delete_{1}",
        "Измменить": f"delete_{2}",
    }))

    await message.answer(
        "ОК, вот список товаров",
    )

    # видео смотреть 1:30:13


# Пример CallbackQuery
@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, db_session: AsyncSession):
    await callback.answer("hello")
    # await callback.message.delete()
    await callback.message.answer("hello")
    print("test")


@admin_router.message(F.text == "Изменить товар")
async def change_product(message: types.Message):
    await message.answer("ОК, вот список товаров")


@admin_router.message(F.text == "Удалить товар")
async def delete_product(message: types.Message):
    await message.answer("Выберите товар(ы) для удаления")


# Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }


@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=CANCEL_BT
    )
    # await message.answer("Д", reply_markup=CANCEL_BT)
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("clear"))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Все действия по созданию товара отменены")


@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"ок, вы вернулись к прошлому шагу")


@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара. " +
                         "Для отмены всех действий введите команду /clear")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара. " +
                         "Для отмены всех действий введите команду /clear")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        await message.answer("Введите корректное значение цены")
        return

    await state.update_data(price=float(message.text))
    await message.answer("Загрузите изображение товара. " +
                         "Для отмены всех действий введите команду /clear")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


# Admin add (назначаем админа через состояние)
class AddAdmin(StatesGroup):
    phone = State()
    confirm = State()

    texts = {
        'AddProduct:phone': 'Введите телефон заново для поиска пользователя:',
    }


@admin_router.message(StateFilter(None), F.text == "Назначить админа")
async def find_user_for_set_admin(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите номер телефон для поиска",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddAdmin.phone)


@admin_router.message(AddAdmin.phone, F.text)
async def set_phone_for_set_admin(
        message: types.Message,
        state: FSMContext,
        db_session: AsyncSession
):
    await state.update_data(phone=message.text)

    user = await get_user_by_phone_number(db_session, message.text)

    text = """
        *** Информация о пользователе ***
    ID: {id}
    Username: {username}
    Telegram ID: {telegram_id}
    Phone number: {phone}
    Created at: {created_at}
    """.format(
        id=user.id,
        username=user.username,
        telegram_id=user.telegram_id,
        phone=user.phone_number,
        created_at=user.created_at,
    )

    await message.answer(text=text)

    await message.answer("Что бы дать админа, введите 'да' " +
                         "Для отмены всех действий введите команду /clear")
    await state.set_state(AddAdmin.confirm)


@admin_router.message(AddAdmin.confirm, F.text)
async def confirm_admin_create(
        message: types.Message,
        state: FSMContext,
        db_session: AsyncSession
):
    if message.text == "да":
        await state.update_data(confirm=message.text)
        data = await state.get_data()
        await message.answer("Права администратора добавлены")
        await set_admin_for_user(db_session, data["phone"], True)
        await state.clear()
    else:
        await message.answer("Введите 'да' для подтверждения " +
                             "Для отмены всех действий введите команду /clear")
