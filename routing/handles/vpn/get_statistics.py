import asyncio

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup

from App import App
from models.User import User
from routing.filter.VpnUserOnlyFilter import VpnUserOnlyFilter
from routing.keyboard.delete_keyboard import get_delete_message_keyboard

router = Router()


@router.callback_query(F.data.startswith("get_statistics"), VpnUserOnlyFilter())
async def get_statistics(callback_query, app: App, vpn_user: User):
    tmp_message = await callback_query.message.answer(
        "⏳ Получение статистики клиента...", parse_mode=None
    )
    await app.logging_service.on_user_request_statistics(vpn_user)

    client = await app.find_clients_by_uuid(vpn_user.uuid)
    if not client or len(client) == 0:
        await callback_query.answer("Клиент не найден.")
        return

    statistics = [
        app.user_repository.get_client_statistics(server, client_data)
        for server, client_data in client.items()
    ]
    statistics = await asyncio.gather(*statistics)

    answer = "Статистика клиента по серверам\n\n"
    for statistics_data in statistics:
        # answer += f"---\n"
        answer += f"✨ {statistics_data.server.readable_name}:\n"
        answer += (
            f"- Статус: {'🟢 Онлайн' if statistics_data.online else '🔴 Оффлайн'}\n"
        )
        answer += f"- Трафик: {'{:.2f}'.format(statistics_data.client.up / (1024 * 1024 * 1024))} ⬆ {'{:.2f}'.format(statistics_data.client.down / (1024 * 1024 * 1024))} ⬇ ГБ\n"
        if len(statistics_data.ips) > 0:
            answer += (
                f"- IP адреса в логе: \n```\n{'\n'.join(statistics_data.ips)}```\n"
            )

        answer += f"\n"

    await tmp_message.delete()
    await callback_query.answer()
    await app.bot.send_message(
        callback_query.from_user.id,
        answer,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_delete_message_keyboard(),
    )
