import asyncio
from typing import List

from aiogram import F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from pydantic import TypeAdapter

from models.UrlKey import UrlKey
from routing.filter.VpnUserOnlyFilter import VpnUserOnlyFilter
from routing.keyboard.delete_keyboard import get_delete_message_keyboard

router = Router()

@router.callback_query(F.data.startswith("get_keys"), VpnUserOnlyFilter())
async def get_keys(callback_query: CallbackQuery, app):
    tmp_message = await app.bot.send_message(callback_query.message.chat.id, "🔍 Поиск ключей...", parse_mode=None)
    user = await app.find_user_by_tgid(callback_query.from_user.id)
    await app.logging_service.on_user_request_keys(user)

    if not user:
        await callback_query.answer("⛔ Пользователь не найден.", show_alert=True)
        return

    found_clients = await app.find_users_key_by_uuid(user.uuid)
    if not found_clients or len(found_clients) == 0:
        await callback_query.answer("⛔ Ключи не найдены для данного пользователя.", show_alert=True)
        return

    urlkey_list_adapter = TypeAdapter(List[UrlKey])
    answer = f"🔑 Найдено {len(found_clients)} ключей для вас:\n\n"
    for urlkey in found_clients:
        answer += f"От сервера ✨**{urlkey.server.readable_name}**: \n```\n{urlkey.url_key}\n```\n\n"
    answer += "⚠️ Скопируйте нужный ключ, сообщение исчезнет через минуту."

    await tmp_message.delete()
    message = await app.bot.send_message(callback_query.message.chat.id, answer, parse_mode=ParseMode.MARKDOWN, reply_markup=get_delete_message_keyboard())
    await callback_query.answer()

    # Delete the callback query message after minute
    await asyncio.sleep(60)
    try:
        await message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")
