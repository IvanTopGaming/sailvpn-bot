import asyncio
from typing import List, Any, Coroutine, Dict

from py3xui import Client
from requests import session

from models.ClientIdentity import ClientIdentity
from models.ClientStatistics import ClientStatistics
from models.Server import Server
from models.UrlKey import UrlKey
from models.User import User
import json


class UsersRepository:
    def __init__(self, file = "config/users.json"):
        self.file = file
        self.allowed_protocols = ["vless"]

    def list_users(self) -> List[User]:
        with open(self.file, "r") as f:
            data_json = json.load(f)
        return [User.model_validate(user) for user in data_json]

    def has_user_with_tgid(self, tgid: int) -> bool:
        users = self.list_users()
        return any(user.tgid == tgid for user in users)

    def find_user_by_tgid(self, tgid: int) -> User | None:
        users = self.list_users()
        for user in users:
            if user.tgid == tgid:
                return user
        return None

    async def find_clients_by_uuid(self, servers: List[Server], uuid: str) -> Dict[Server, ClientIdentity]:
        found_clients_tasks = []
        for server in servers:
            found_clients_tasks.append(self.find_client_in_server_by_uuid(server, uuid))
        found_clients_tasks = await asyncio.gather(*found_clients_tasks)

        found_clients = {}
        for task in found_clients_tasks:
            if task:
                found_clients[task.server] = task

        return found_clients

    async def find_client_in_server_by_uuid(self, server: Server, uuid: str) -> ClientIdentity | None:
        async with server.new_session() as session:
            for inbound in await session.inbound.get_list():
                if inbound.protocol not in self.allowed_protocols:
                    continue
                for client in inbound.settings.clients:
                    if client.id == uuid:
                        return ClientIdentity(
                            server=server,
                            inbound=inbound,
                            client=client,
                        )
        return None

    async def find_client_keys_by_uuid(self, servers: List[Server], uuid: str) -> List[UrlKey]:
        found_clients_tasks = []
        for server in servers:
            found_clients_tasks.append(self.find_client_key_in_server_by_uuid(server, uuid))
        found_clients_tasks = await asyncio.gather(*found_clients_tasks)

        found_clients = []
        for task in found_clients_tasks:
            found_clients.extend(task)

        return found_clients

    async def find_client_key_in_server_by_uuid(self, server: Server, uuid: str) -> List[UrlKey]:
        found_clients = []
        async with server.new_session() as session:
            for inbound in await session.inbound.get_list():
                if inbound.protocol not in self.allowed_protocols:
                    continue
                for client in inbound.settings.clients:
                    if client.id == uuid:
                        found_clients.append(UrlKey(
                            server=server,
                            name=client.email,
                            url_key=server.build_url_key(inbound, client),
                        ))

        return found_clients

    async def find_user_by_uuid(self, uuid: str) -> User | None:
        for user in self.list_users():
            if user.uuid == uuid:
                return user
        return None

    """def get_users_statistics(self, user_uuid):
        client = self.find_user_by_uuid(user_uuid)
        found_clients = []
        async with server.new_session() as session:
            for inbound in await session.inbound.get_list():
                if inbound.protocol not in self.allowed_protocols:
                    continue
                for client in inbound.settings.clients:
                    if client.id == uuid:"""

    async def get_client_statistics(self, server: Server, client_identity: ClientIdentity) -> ClientStatistics | None:
        async with server.new_session() as session:
            client = await session.client.get_by_email(client_identity.client.email)
            online_clients = await session.client.online()
            known_ips = await session.client.get_ips(email=client.email)
            if type(known_ips) is str:
                known_ips = json.loads(known_ips)

            return ClientStatistics(
                server=server,
                inbound=client_identity.inbound,
                client=client,
                online=client.email in online_clients,
                ips=known_ips,
            )
