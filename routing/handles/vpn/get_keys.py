import asyncio
from typing import List

from aiogram import F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from pydantic import TypeAdapter

from App import App
from models.UrlKey import UrlKey
from models.User import User
from routing.filter.VpnUserOnlyFilter import VpnUserOnlyFilter
from routing.keyboard.additional_key_selection_keyboard import get_additional_key_selection_keyboard
from routing.keyboard.delete_keyboard import get_delete_message_keyboard


router = Router()

@router.callback_query(F.data.startswith("get_keys"), VpnUserOnlyFilter())
async def get_keys(callback_query: CallbackQuery, app: App, vpn_user: User):
    tmp_message = await app.bot.send_message(callback_query.message.chat.id, "🔍 Поиск ключей...", parse_mode=None)
    await app.logging_service.on_user_request_keys(vpn_user)

    additional_key = None
    key_to_search = None
    if callback_query.data == "get_keys:main":
        key_to_search = vpn_user.uuid
    elif callback_query.data.startswith("get_keys:"):
        key_to_search = callback_query.data.split(":")[1]
        for _additional_key in vpn_user.additional_keys or []:
            if _additional_key.uuid == key_to_search:
                additional_key = _additional_key
                break
        if not additional_key:
            await tmp_message.delete()
            await callback_query.answer("⛔ Дополнительный ключ не найден.", show_alert=True)
            return

    if not vpn_user.additional_keys:
        key_to_search = vpn_user.uuid

    if vpn_user.additional_keys and not key_to_search:
        await tmp_message.delete()
        await callback_query.answer()
        await callback_query.message.answer(
            "❔ У вас есть дополнительные ключи, какой бы вы хотели получить, свой - основной или какой то из дополнительных?",
            show_alert=True,
            reply_markup=get_additional_key_selection_keyboard(vpn_user)
        )
        return

    if ':' in callback_query.data:
        await callback_query.message.delete()

    found_clients = await app.find_users_key_by_uuid(key_to_search)
    if not found_clients or len(found_clients) == 0:
        await callback_query.answer("⛔ Ключи не найдены для данного пользователя.", show_alert=True)
        return

    urlkey_list_adapter = TypeAdapter(List[UrlKey])
    answer = f"🔑 Найдено {len(found_clients)} ключей для {'вас' if not additional_key else "дополнительного подключения *" + additional_key.name + "*"}:\n\n"
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
