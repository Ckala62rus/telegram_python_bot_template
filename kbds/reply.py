from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Первая кнопка"),
            KeyboardButton(text="Вторая кнопка"),
        ],
        [
            KeyboardButton(text="Третья кнопка"),
            KeyboardButton(text="Четвертая кнопка"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

