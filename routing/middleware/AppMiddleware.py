from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class AppMiddleware(BaseMiddleware):
    def __init__(self, app):
        self.app = app

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['app'] = self.app
        return await handler(event, data)
