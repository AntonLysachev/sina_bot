from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_grade_keyboard():
    keyboard = InlineKeyboardBuilder()
    for i in range(1, 6):
        data = f'{{"name": "grade", "params": {{"grade": {i}}}}}'
        keyboard.add(InlineKeyboardButton(text='\u2b50\ufe0f' * i, callback_data=data))
    return keyboard.adjust(1).as_markup()
