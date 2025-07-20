from typing import List

from py3xui import Client, Inbound
from pydantic import BaseModel

from models.Server import Server


class ClientStatistics(BaseModel):
    server: Server
    inbound: Inbound
    client: Client
    online: bool
    ips: List[str]
