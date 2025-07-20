from dataclasses import dataclass


@dataclass
class ClientSearchResult:
    def __init__(self, server, inbound, client):
        self.server = server
        self.inbound = inbound
        self.client = client
