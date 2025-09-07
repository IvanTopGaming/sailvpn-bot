from typing import List
from models.Server import Server
import json


class ServersRepository:
    def __init__(self, file="config/servers.json"):
        self.file = file

    def list_servers(self) -> List[Server]:
        with open(self.file, "r") as f:
            data_json = json.load(f)
        return [Server.model_validate(server) for server in data_json]
