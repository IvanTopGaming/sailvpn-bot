import logging
from typing import Dict

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from py3xui import Client

from data.repository.UsersRepository import UsersRepository
from models.ClientIdentity import ClientIdentity
from models.Config import Config
from models.Server import Server
from models.UrlKey import UrlKey
from models.User import User
from routing.filter.VpnUserOnlyFilter import VpnUserOnlyFilter
from routing.handles import handle_names
from data.repository.ServersRepository import ServersRepository
from routing.middleware.AppMiddleware import AppMiddleware


class App:
    def __init__(self):
        self.config = Config.load_from_file("config/config.json")
        self.logger = logging.getLogger(__name__)
        self.bot = Bot(
            token=self.config.telegram_token,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
        )

        self.server_repository = ServersRepository(file="config/servers.json")
        self.user_repository = UsersRepository(file="config/users.json")

        self.dispatcher = Dispatcher(bot=self.bot)

        self.vpn_user_only_filter = VpnUserOnlyFilter()

        for handler in handle_names:
            self.logger.debug("Including router " + handler)
            router: Router = __import__('routing.handles.' + handler, fromlist=['router']).router

            # Process router
            router.message.outer_middleware(AppMiddleware(self))
            router.callback_query.outer_middleware(AppMiddleware(self))

            self.dispatcher.include_router(router)

    async def run(self):
        await self.dispatcher.start_polling(self.bot)


    async def find_users_key_by_uuid(self, uuid: str) -> list[UrlKey]:
        servers = self.server_repository.list_servers()
        found_clients = await self.user_repository.find_client_keys_by_uuid(servers, uuid)
        return found_clients

    async def find_user_uuid_by_tgid(self, tgid: str) -> User:
        found_client = await self.user_repository.find_user_by_uuid(tgid)
        return found_client

    async def find_clients_by_uuid(self, uuid: str) -> Dict[Server, ClientIdentity]:
        servers = self.server_repository.list_servers()
        found_clients = await self.user_repository.find_clients_by_uuid(servers, uuid)
        return found_clients
