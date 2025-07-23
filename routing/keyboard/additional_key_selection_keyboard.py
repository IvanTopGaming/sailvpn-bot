from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.User import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_additional_key_selection_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔑 Основной ключ", callback_data=f"get_keys:main")

    for key in user.additional_keys:
        keyboard.button(text=f"🗝️ Дополнительный: {key.name}", callback_data=f"get_keys:{key.uuid}")

    keyboard.button(text="❌ Отмена", callback_data="remove_message")
    keyboard.adjust(1)
    return keyboard.as_markup()