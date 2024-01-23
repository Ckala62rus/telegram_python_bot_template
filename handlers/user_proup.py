from string import punctuation

from aiogram import types, Router
from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'чушпан', 'хуй'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(message.text.lower().split()):
        await message.answer(f"{message.from_user.username}, соблюдай порядок в чате пёс!")
        await message.delete()
        # if you need ban person
        # await message.chat.ban(message.from_user.id)
