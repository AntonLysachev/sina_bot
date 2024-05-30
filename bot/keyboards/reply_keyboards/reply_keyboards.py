from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Кофе для друзей'),
     KeyboardButton(text='Оставьте отзыв')],
    [KeyboardButton(text='Контакты'),
     KeyboardButton(text='Обновить данные')],],
    resize_keyboard=True)


send_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить", request_contact=True)]],
    resize_keyboard=True)
