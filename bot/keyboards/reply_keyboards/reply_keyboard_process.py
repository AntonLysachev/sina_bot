from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.messages import cups
from bot.keyboards.inline_keyboards.inline_keyboards import inline_registration, inline_contacts, inline_cancal, inline_update
from bot.review import Review
from bot.db.ORM import get_customer_by_chat_id
from bot.registratin import Registration


reply = Router()


@reply.message(F.text == 'Контакты')
async def handle_contacts(message: Message) -> None:
    await message.answer('Контакты', reply_markup=inline_contacts)


@reply.message(F.text == 'Оставьте отзыв')
async def handle_comment(message: Message, state: FSMContext):
    await state.set_state(Review.text)
    await message.answer("Помоги нам стать лучше! Оставь свой отзыв:", reply_markup=inline_cancal)


@reply.message()
async def handle_all_messages(message: Message, state: FSMContext) -> None:

    chat_id = message.chat.id
    button = buttons.get(message.text)
    customer = await get_customer_by_chat_id(chat_id)
    if button:
        if customer:
            await button(message)
        else:
            await state.set_state(Registration.phone)
            await message.answer('Вы не зарегистрированы в нашем боте.\nДавайте это исправим?', reply_markup=inline_registration)
    else:
        await message.reply('Произошла ошибка. Отправьте свое сообщение еще раз.')


async def contacts(message: Message):
    await message.answer('Контакты', reply_markup=inline_contacts)


async def coffee_for_friends(message: Message) -> None:
    await cups(message)


async def update_data(message: Message):
    await message.answer('Какие данные вы хотите обновить?', reply_markup=inline_update)


buttons = {
    'Кофе для друзей': coffee_for_friends,
    'Обновить данные': update_data,
}
