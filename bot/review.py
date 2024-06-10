import os
from dotenv import load_dotenv
from bot.db import orm
from aiogram import Router
from aiogram.types import Message
from bot.keyboards import builder
from bot.keyboards.inline_keyboards.inline_keyboards import inline_contacts, inline_cancal
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

review = Router()


class Review(StatesGroup):
    text = State()
    grade = State()


@review.message(Review.text)
async def review_start(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    data = await state.get_data()
    grade = data.get("grade", None)
    text = data.get("text", None)
    if grade:
        chat_id = message.chat.id
        customer_id = await orm.get_customer_id_by_chat_id(chat_id)
        await orm.add_review(grade, customer_id, 'only_grade', text)
        await message.answer('Спасибо за вашу обратную связь! Нам важно каждое мнение. Надеемся, что наша дружба станет крепче!')
        await state.clear()
    else:
        await message.answer('На сколько звездочек вы оцениваете наше качество обслуживания?', reply_markup=builder.get_grade_keyboard())


async def review_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    grade = data.get('grade')
    if grade < 4:
        await prompt_for_review(message, state)
    else:
        chat_id = message.chat.id
        customer_id = await orm.get_customer_id_by_chat_id(chat_id)
        await message.answer("Помоги нам стать лучше! Оставь свой отзыв в социальных сетях:", reply_markup=inline_contacts)
        await orm.add_review(grade, customer_id, 'only_grade')
        await state.clear()


async def prompt_for_review(message: Message, state: FSMContext) -> None:
    await state.set_state(Review.text)
    await message.answer("Помоги нам стать лучше! Оставь свой отзыв:", reply_markup=inline_cancal)


async def send_bed_review(text, grade, phone):
    admins = await orm.get_admins()
    async with Bot(token=TELEGRAM_TOKEN) as bot:
        for admin in admins:
            await bot.send_message(admin, f'!!!!!ПЛОХОЙ ОТЗЫВ!!!!!!\n\nНомер клиента: {phone}\n\nОценка: {grade}\n\nОтзыв:\n{text}')
