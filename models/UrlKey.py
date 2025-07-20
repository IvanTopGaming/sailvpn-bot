from py3xui import Inbound
from pydantic import BaseModel

from models.Server import Server


class UrlKey(BaseModel):
    server: Server
    name: str
    url_key: str
