import json
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from bot.keyboards.reply_keyboards.reply_keyboards import main_keyboard, send_keyboard
from bot.keyboards.inline_keyboards.inline_keyboards import inline_update_name, inline_update_phone, inline_registration, inline_cancal
from bot.db import orm
from bot.update import Update
from bot.review import save_only_grade_review, save_full_review


callbacks = Router()


@callbacks.callback_query(F.data.startswith('{"name":'))
async def response_to_callback(call: CallbackQuery, state: FSMContext):
    func = json.loads(call.data)
    message = call.message
    name = func.get('name')
    params = func.get('params')
    if params:
        callback_func = callback.get(name)
        await callback_func(message, state, **params)
    else:
        callback_func = callback.get(name)
        await callback_func(message)


@callbacks.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Ждем вас в Sina Coffee', reply_markup=main_keyboard)
    await state.clear()


@callbacks.callback_query(F.data == '_cancel')
async def _cancel(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("""
Мы хотим подружиться с вами! С
радостью ждем вас в нашей кофейне по
адресу:
📍ул. Айбека 4А, ориентир: метро Айбек
                              """, reply_markup=main_keyboard)
    await state.clear()


@callbacks.callback_query(F.data == 'prompt_for_phone_update')
async def prompt_for_phone_update(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Update.phone)
    await call.message.answer('Отправте контакт или введите номер телефона вручную', reply_markup=inline_registration)


@callbacks.callback_query(F.data == 'prompt_for_name_update')
async def prompt_for_name_update(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Update.name)
    await call.message.answer('Введите свои - фамилия имя:', reply_markup=inline_cancal)


async def send_phone(message: Message) -> None:
    await message.answer("Нажмите кнопку 'Отправить', чтобы отправить ваш номер телефона.", reply_markup=send_keyboard)


async def enter_phone_manual(message: Message) -> None:
    await message.answer("Отлично. Один шаг и мы у цели\nВведите номер телефона в формате +998123456789")


async def grade(message: Message, state: FSMContext, **kwargs) -> None:
    chat_id = message.chat.id
    grade = kwargs.get('grade')
    await state.update_data(grade=grade)
    data = await state.get_data()
    grade = data.get("grade", None)
    text = data.get("text", None)
    if text:
        await save_full_review(message, state, grade, text, chat_id)
    else:
        await save_only_grade_review(message, state)


async def get_phone(message: Message) -> None:
    chat_id = message.chat.id
    phone = await orm.get_phone_by_chat_id(chat_id)
    await message.answer(f'Ваш номер в нашей "Системе дружбы": {phone}', reply_markup=inline_update_phone)


async def get_name(message: Message) -> None:
    chat_id = message.chat.id
    full_name = await orm.get_full_name_by_chat_id(chat_id)
    await message.answer(f'Ваше имя в нашей "Системе дружбы": {full_name}', reply_markup=inline_update_name)


callback = {
    'send_phone': send_phone,
    'enter_phone_manual': enter_phone_manual,
    'grade': grade,
    'get_phone': get_phone,
    'get_name': get_name,
    'cancel': _cancel,
    # 'yes': yes,
    # 'no': no,
    # 'add_grade_review_text': add_grade_review_text,
}
