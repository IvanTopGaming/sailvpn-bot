from aiogram.enums import ParseMode

from models.Config import Config


class Tglogger:
    def __init__(self, bot, config: Config):
        self.bot = bot
        self.config = config

    async def log(self, message: str, parse_mode: ParseMode | None = None):
        if not self.bot:
            return
        try:
            await self.bot.send_message(chat_id=self.config.telegram_logs_chat_id, text=message, parse_mode=parse_mode)
        except Exception as e:
            print(f"Failed to send message: {e}")
