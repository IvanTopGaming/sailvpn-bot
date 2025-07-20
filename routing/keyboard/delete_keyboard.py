from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_delete_message_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="️❌ Скрыть сейчас", callback_data="remove_message")
    keyboard.adjust(1)
    return keyboard.as_markup()
