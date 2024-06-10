from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from bot.keyboards.inline_keyboards.inline_keyboards import inline_cancal
from bot.keyboards.reply_keyboards.reply_keyboards import main_keyboard
from bot.poster import API
from .db import orm
from bot.utils import phone_input


registration = Router()
api = API()


class Registration(StatesGroup):
    phone = State()


@registration.message(Registration.phone)
async def registration_customer(message: Message, state: FSMContext):
    phone_number = await phone_input(message)
    if phone_number:
        client = await api.get_customer_by_phone(phone_number)
        if client:
            chat_id = message.chat.id
            poster_id = int(client['client_id'])
            group_name = client['client_groups_name']
            firstname = client['firstname']
            lastname = client['lastname']
            fullname = f'{lastname} {firstname}'
            await orm.add_customer(phone_number, chat_id, poster_id, group_name, firstname, lastname)
            await message.answer(text=f'Спасибо за подписку, дорогой друг!🧡.\n'
                                      f'Ваши данные в Системе Дружбы:\nИмя: {fullname}\nНомер телефона: {phone_number}',
                                 reply_markup=main_keyboard)
            await state.clear()
            await api.add_incoming_order(poster_id)
        else:
            await message.answer(text="""
К сожалению, такого контакта нет у нас в друзьях🥹.
Проверьте правильность отправленного номера
или попробуйте ввести его вручную в формате: +998987654321

Или, возможно, вы еще не разу не были в нашей кофейне?
Напоминаем: чтобы зарегистрироваться в Системе Дружбы,
нужно совершить первую покупку в нашей кофейне по адресу:
📍ул. Айбека 4А, ориентир: метро Айбек

Если у вас остались вопросы, вы можете обратиться за помощью к администратору.
                    """, reply_markup=inline_cancal)
