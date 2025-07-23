from aiogram import types
from aiogram.filters import BaseFilter


class VpnUserOnlyFilter(BaseFilter):
    """
    Filter to allow only VPN users.
    """

    async def __call__(self, update: types.Update, app):
        user_id = update.from_user.id
        user = app.user_repository.find_user_by_tgid(user_id)
        if user:
            return {"vpn_user": user}

        await update.answer("⛔ Доступ к боту запрещен, вы не являетесь доверенным пользователем. Если вы ожидали его получить, обратитесь в поддержку.", parse_mode=None)
        return False
