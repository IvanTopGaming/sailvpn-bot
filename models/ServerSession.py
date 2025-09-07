from py3xui import AsyncApi


class ServerSession:
    def __init__(self, server):
        self.server = server

    async def __aenter__(self) -> AsyncApi:
        self.session = AsyncApi(
            host=self.server.host,
            username=self.server.username,
            password=self.server.password,
            use_tls_verify=self.server.use_tls_verify,
        )
        await self.session.login()
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        if hasattr(self, "session"):
            self.session = None
        return False
