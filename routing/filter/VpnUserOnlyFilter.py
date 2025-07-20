from aiogram import types
from aiogram.filters import BaseFilter


class VpnUserOnlyFilter(BaseFilter):
    """
    Filter to allow only VPN users.
    """

    async def __call__(self, update: types.Update, app):
        user = update.from_user.id
        if app.user_repository.has_user_with_tgid(user):
            return True

        await update.answer("⛔ Доступ к боту запрещен, вы не являетесь доверенным пользователем. Если вы ожидали его получить, обратитесь в поддержку.", parse_mode=None)
        return False
