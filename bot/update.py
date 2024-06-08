from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.db.ORM import update_customers_name, update_customer_phone, get_customer_by_chat_id
from bot.poster import API
from bot.utils import phone_input
from bot.keyboards.inline_keyboards.inline_keyboards import inline_registration
from bot.keyboards.reply_keyboards.reply_keyboards import main_keyboard

update = Router()
api = API()

class Update(StatesGroup):
    phone = State()
    name = State()


@update.message(Update.name)
async def update_name(message: Message, state: FSMContext) -> None:

    chat_id = message.chat.id
    customer = await get_customer_by_chat_id(chat_id)
    poster_id = customer.poster_id
    customer_id = customer.id
    new_name = message.text
    poster_id = await api.update_customer_info(client_id=poster_id, client_name=new_name)
    customer = await api.get_customer_by_id(poster_id)
    await update_customers_name(customer['firstname'], customer['lastname'], customer_id)
    name = f'{customer["lastname"]} {customer["firstname"]}'
    if name:
        await message.answer(f'Мы Изменили имя на: {name}')
    else:
        await message.answer('Произошла ошибка, попробуйте позже')
    await state.clear()


@update.message(Update.phone)
async def update_phone(message: Message, state: FSMContext) -> None:
    new_phone = await phone_input(message)
    if new_phone:
        is_exist = await api.get_customer_by_phone(new_phone)
        if is_exist:
            await message.answer('Такой номер уже зарегестрирован', reply_markup=inline_registration)
        else:
            chat_id = message.chat.id
            customer = await get_customer_by_chat_id(chat_id)
            poster_id = customer.poster_id
            customer_id = customer.id
            poster_id = await api.update_customer_info(client_id=poster_id, phone=new_phone)
            customer = await api.get_customer_by_id(poster_id)
            phone = customer['phone']
            if phone:
                await update_customer_phone(phone, customer_id)
                await message.answer(f'Мы изменили номер на: {phone}', reply_markup=main_keyboard)
            else:
                await message.answer('Произошла ошибка, попробуйте позже')
            await state.clear()
