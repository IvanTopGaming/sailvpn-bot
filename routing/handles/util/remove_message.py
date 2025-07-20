from aiogram import F, Router

from routing.filter.VpnUserOnlyFilter import VpnUserOnlyFilter


router = Router()

@router.callback_query(F.data.startswith("remove_message"), VpnUserOnlyFilter())
async def remove_message(callback_query):
    try:
        await callback_query.message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")
    await callback_query.answer("Сообщение удалено.")