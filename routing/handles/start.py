from aiogram import Router
from aiogram.filters import CommandStart

from routing.filter.VpnUserOnlyFilter import VpnUserOnlyFilter
from routing.keyboard.start_keyboard import get_start_keyboard

router = Router()


@router.message(CommandStart(), VpnUserOnlyFilter())
async def bot_start(message):
    await message.answer(
        "Привет👋, я тебя знаю, можешь пользоваться моими функциями.\nЧто хочешь сделать?",
        parse_mode=None,
        reply_markup=get_start_keyboard(),
    )
