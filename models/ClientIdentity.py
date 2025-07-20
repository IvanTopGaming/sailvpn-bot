from py3xui import Inbound, Client
from pydantic import BaseModel

from models.Server import Server


class ClientIdentity(BaseModel):
    server: Server
    inbound: Inbound
    client: Client
