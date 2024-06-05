import pytest
from bot.commands.start import cmd_start
from unittest.mock import AsyncMock
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from bot.keyboards.inline_keyboards.inline_keyboards import inline_registration
from .utils import TEST_USER, TEST_USER_CHAT
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@pytest.mark.asyncio
async def message_state(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id)
    )
    return message, state

@pytest.mark.asyncio
async def test_start_hendler(storage, bot):
    message, state = await message_state(storage, bot)
    await cmd_start(message, state)
    message.answer.assert_called_with("""
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


@pytest.mark.asyncio
async def test_inline_keyboard(storage, bot):
    message, state = await message_state(storage, bot)
    expected_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить номер телефона", callback_data='{"name": "send_phone"}')],
        [InlineKeyboardButton(text="Ввести номер вручную", callback_data='{"name": "enter_phone_manual"}')],
        [InlineKeyboardButton(text="Отмена", callback_data='_cancel')]
    ])

    await cmd_start(message, state)
    _, kwargs = message.answer.call_args
    actual_markup = kwargs['reply_markup']

    assert actual_markup == expected_markup
