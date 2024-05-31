import csv
import os
import re
from aiogram.types import Message
from bot.keyboards.inline_keyboards.inline_keyboards import inline_cancal

path = os.path.dirname(os.path.dirname(__file__))


def get_normalized_products_name() -> dict:

    with open(os.path.join(path, 'products.csv'), 'r', encoding='utf-8-sig') as csvfile:
        data = csv.reader(csvfile)
        map_data = {}

        for row in data:
            key, value = row[0].split(';')
            map_data[key] = value
        return map_data


products = get_normalized_products_name()


async def phone_input(message: Message) -> str | None:
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    else:
        phone = message.text
        phone_number = phone if re.match(r'^\+\d{11,}$', phone) else None
        if phone_number is None:
            await message.answer('ОЙ! Не верный формат. Проверьте правильность введеных данных и отправте снова', reply_markup=inline_cancal)
            return None
    return phone_number
