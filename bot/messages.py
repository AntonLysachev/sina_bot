import bot.poster as poster
from bot.utils import products
from aiogram.types import Message
from bot.db.ORM import get_poster_id_by_chat_id


async def to_present(poster_id):

    count = 0
    present_info = {
        'to_cup': 0,
        'cups': 0
    }

    client = poster.get_customer_by_id(poster_id)
    accumulation_products = client['accumulation_products']
    prize_products = client['prize_products']

    present_info['cups'] = len(prize_products)

    if accumulation_products:
        for group in accumulation_products.values():
            if group['promotion_id'] == 1:
                for cup in group['products']:
                    count += cup['count']

    present_info['to_cup'] = 4 - count

    return present_info


async def cups(message: Message) -> None:
    chat_id = message.chat.id
    poster_id = await get_poster_id_by_chat_id(chat_id)
    await message.answer(await get_presemt_message(poster_id))


async def get_buy_message(transaction_id: int) -> str:
    buy_products = poster.get_product_in_receipt(transaction_id)
    name_of_product = ''
    for name, count in buy_products.items():
        normalized_name = products.get(name)
        if normalized_name:
            name_of_product = f'{name_of_product}{normalized_name} - {count}\n'
        else:
            name_of_product = f'{name_of_product}{name} - {count}\n'

    return f'Вы приобрели:\n{name_of_product}'


async def get_presemt_message(poster_id: int) -> str:
    present_info = await to_present(poster_id)
    to_cup = present_info['to_cup']
    cups = present_info['cups']
    if cups == 0:
        return f'Еще {to_cup} {await get_ending_cup(to_cup)} и мы подарим вам 1 бесплатный напиток🎁'
    if cups == 1 and to_cup == 4:
        return f'А у вас уже {await get_ending_accumulated(cups)} {cups} {await get_ending_drink(cups)}.'
    return f'А у вас уже {await get_ending_accumulated(cups)} {cups} {await get_ending_drink(cups)}.\nЕще {to_cup} {await get_ending_cup(to_cup)} и мы подарим вам 1 бесплатный напиток.'


async def get_ending_drink(quantity_cups: int) -> str:

    units = quantity_cups % 10
    if units == 0 or (4 < quantity_cups < 21):
        word = 'бесплатных напитков'
    elif units == 1:
        word = 'бесплатный напиток'
    else:
        word = 'бесплатных напитка'
    return word


async def get_ending_cup(quantity_cups: int) -> str:

    units = quantity_cups % 10
    if units == 0 or (4 < quantity_cups < 21):
        word = 'выпитых стаканчиков'
    elif units == 1:
        word = 'выпитый стаканчик'
    else:
        word = 'выпитых стаканчика'
    return word


async def get_ending_accumulated(quantity_cups: int) -> str:

    units = quantity_cups % 10
    if units == 0 or (4 < quantity_cups < 21):
        word = 'накоплено'
    elif units == 1:
        word = 'накоплен'
    else:
        word = 'накоплено'
    return word
