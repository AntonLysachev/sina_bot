from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from bot.keyboards.inline_keyboards.inline_keyboards import inline_registration
from bot.keyboards.reply_keyboards.reply_keyboards import main_keyboard
from bot.registratin import Registration as Reg
from bot.db.ORM import get_customer_by_chat_id

start = Router()


@start.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    customer = await get_customer_by_chat_id(chat_id)
    if customer is None:
        await state.set_state(Reg.phone)
        await message.answer("""
Друг, Sina Coffee приветствует тебя!🧡

Данный бот создан для того, чтобы
следить за количеством выпитых
стаканчиков. Подпишитесь и будьте
всегда в курсе ваших бесплатных
напитков и действующих акций!

Чтобы зарегистрироваться в Системе Дружбы,
нужно совершить первую покупку в нашей кофейне по адресу:
📍ул. Айбека 4А, ориентир: метро Айбек

Для того, чтобы мы могли поддерживать
связь, поделитесь с нами номером
телефона, указанным при регистрации в
кофейне.
                             """, reply_markup=inline_registration)
    else:
        await message.answer('Друг, Sina Coffee приветствует тебя!🧡', reply_markup=main_keyboard)
