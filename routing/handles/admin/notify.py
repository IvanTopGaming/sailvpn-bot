from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from App import App
from routing.filter.AdminOnlyFilter import AdminOnlyFilter
from utils.uuid import is_valid_uuid

router = Router()


@router.message(Command("notify"), AdminOnlyFilter())
async def notify_user(message: Message, app: App):
    user_to_notify = (
        message.text.split(maxsplit=2)[1] if len(message.text.split()) > 1 else None
    )
    notification_text = (
        message.text.split(maxsplit=2)[2] if len(message.text.split()) > 2 else None
    )
    if not user_to_notify:
        await message.answer("⛔ Пожалуйста, укажите пользователя для уведомления.")
        return

    if is_valid_uuid(user_to_notify):
        user_to_notify = (await app.find_user_by_uuid(user_to_notify)).tgid
    elif user_to_notify.isdigit():
        user_to_notify = int(user_to_notify)
        if not app.user_repository.has_user_with_tgid(user_to_notify):
            await message.answer(
                "⚠️ Пользователь с таким Telegram ID не найден в базе пользователей."
            )
    else:
        await message.answer(
            "⛔ Пожалуйста, укажите корректный UUID пользователя или его Telegram ID."
        )
        return

    if not notification_text or len(notification_text) < 3:
        await message.answer(
            "⛔ Пожалуйста, укажите текст уведомления (минимум 3 символа) в формате Markdown."
        )
        return

    tmp_message = await message.answer(
        f"⏳ Отправка уведомления пользователю {user_to_notify}..."
    )

    try:
        sent_notification = await app.bot.send_message(
            user_to_notify, notification_text
        )
    except Exception as e:
        await tmp_message.edit_text(
            f"⛔ Ошибка при отправке уведомления пользователю {user_to_notify}: {str(e)}"
        )
        return
    else:
        await tmp_message.edit_text(
            f"✅ Уведомление успешно отправлено пользователю {user_to_notify}.\n\nТекст:\n```\n{notification_text}\n```\nUnnotify id: `{sent_notification.message_id}@{sent_notification.chat.id}`",
            parse_mode=ParseMode.MARKDOWN,
        )

    # await message.answer(f"{user_to_notify} {message.entities}")


@router.message(Command("unnotify"), AdminOnlyFilter())
async def remove_notification(message: Message, app: App):
    unnotify_id = (
        message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    )
    if not unnotify_id:
        await message.answer("⛔ Пожалуйста, укажите ID уведомления для удаления.")
        return

    try:
        await app.bot.delete_message(
            chat_id=unnotify_id.split("@")[1], message_id=int(unnotify_id.split("@")[0])
        )
    except Exception as e:
        await message.answer(f"⛔ Ошибка при удалении уведомления: {str(e)}")
    else:
        await message.answer(
            f"✅ Уведомление с ID `{unnotify_id}` успешно удалено.",
            parse_mode=ParseMode.MARKDOWN,
        )
