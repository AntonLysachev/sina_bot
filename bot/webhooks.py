from aiohttp import web
from aiogram import Bot
import hashlib
import os
from dotenv import load_dotenv
from bot import poster
from bot.db.ORM import get_chat_id_by_poster_id
from bot.messages import get_buy_message, get_presemt_message
from bot.keyboards import builder

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

webhooks = web.RouteTableDef()


@webhooks.post('/webhooks')
async def process_sale_info(request):
    webhook = await request.json()
    print('!!!!!!!')
    try:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # account = webhook['account']
        object = webhook['object']
        object_id = webhook['object_id']
        action = webhook['action']
        # time = webhook['time']
        # secret = os.getenv('POSTER_SECRET')
        # verify = webhook['verify']
        # signature_string = f"{account};{object};{object_id};{action};{time};{secret}"
        # signature = hashlib.md5(signature_string.encode()).hexdigest()
        entity = entitys.get(object)
        if entity:
            function = entity.get(action)
            if function:
                function(object_id)
    except Exception as e:
        return web.Response(text='ok', status=200)
    return web.Response(text='ok', status=200)


async def closed(object_id: int):
    receipt = await poster.get_receipt(object_id)
    poster_id = receipt['client_id']
    chat_id = await get_chat_id_by_poster_id(poster_id)
    if chat_id:
        async with Bot(token=TELEGRAM_TOKEN) as bot:
            buy_message = await get_buy_message(object_id)
            present_message = await get_presemt_message(poster_id)
            await bot.send_message(chat_id, f'{buy_message}\n{present_message}')
            await bot.send_message(chat_id, 'На сколько звездочек вы оцениваете наше качество обслуживания?', reply_markup=builder.get_grade_keyboard())


transactions = {
    'closed': closed
}

entitys = {
    'transaction': transactions
}
