from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить номер телефона", callback_data='{"name": "send_phone"}')],
    [InlineKeyboardButton(text="Ввести номер вручную", callback_data='{"name": "enter_phone_manual"}')],
    [InlineKeyboardButton(text="Отмена", callback_data='_cancel')]
])

inline_cancal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data='cancel')]
])

inline_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Instagram', url="https://www.instagram.com/sinacoffee.uz?igsh=OGZrMWxxbGE0aTFr")],
    [InlineKeyboardButton(text='Yandex', url="https://yandex.ru/maps/org/202556629894")],
    [InlineKeyboardButton(text="Google", url="https://maps.app.goo.gl/14DSs8iN62K2UF5y8?g_st=it")],
    [InlineKeyboardButton(text='2GIS', url="https://2gis.ru/tashkent/geo/70000001075241429/69.272959,41.298072")],
])

inline_update = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Имя', callback_data='{"name": "get_name"}')],
    [InlineKeyboardButton(text='Телефоне', callback_data='{"name": "get_phone"}')],
    [InlineKeyboardButton(text="Отмена", callback_data='cancel')],
])

inline_update_phone = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='prompt_for_phone_update')],
    [InlineKeyboardButton(text="Отмена", callback_data='cancel')],
])

inline_update_name = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='prompt_for_name_update')],
    [InlineKeyboardButton(text="Отмена", callback_data='cancel')],
])
