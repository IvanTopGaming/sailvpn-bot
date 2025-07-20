from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="️🔑 Получить ключи", callback_data="get_keys")
    keyboard.button(text="📊 Посмотреть статистику", callback_data="get_statistics")
    keyboard.adjust(1)
    return keyboard.as_markup()
