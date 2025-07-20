import asyncio
import logging
import sys
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from App import App
from data.repository.ServersRepository import ServersRepository
from utils.connection_string import get_connection_string
from utils.py3xui import find_client_by_uid


app = App()
dp = Dispatcher()

@dp.message(CommandStart())
async def bot_start(message):
    servers_repo = ServersRepository(file="config/servers.json")
    servers = servers_repo.list_servers()
    tmp_message = await message.answer("Searching for client...", parse_mode=None)

    found_clients = await find_client_by_uid(servers, "942ea5e5-daa6-439c-a987-d2229ed43460")

    text = [found_client.server.readable_name + ': ' + get_connection_string(
        inbound=found_client.inbound,
        user_uuid=found_client.client.id,
        server_host=found_client.server.vless_host,
        server_port=found_client.server.vless_port,
        user_name=found_client.client.email,
        server_name=found_client.server.vless_host
    ) for found_client in found_clients]

    await tmp_message.delete()
    await bot.send_message(tmp_message.chat.id, "\n\n".join(text), parse_mode=None)


async def main() -> None:
    await app.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
