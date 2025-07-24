from aiogram import types
from aiogram.filters import BaseFilter


class AdminOnlyFilter(BaseFilter):
    """
    Filter to allow only admins.
    """

    async def __call__(self, update: types.Update, app):
        user_id = update.from_user.id
        if user_id in app.config.telegram_admins:
            return True

        # await update.answer("⛔ Доступ к боту запрещен.", parse_mode=None)
        return False
