from typing import Optional
from pydantic import BaseModel
from models.ServerSession import ServerSession


class Server(BaseModel):
    host: str
    username: str
    password: str
    conventional_name: str
    readable_name: Optional[str] = None
    use_tls_verify: bool = True
    vless_host: Optional[str] = None
    vless_port: int = 443

    def new_session(self) -> ServerSession:
        return ServerSession(self)

    def build_url_key(self, inbound, client) -> str:
        public_key = inbound.stream_settings.reality_settings.get("settings").get(
            "publicKey"
        )
        website_name = inbound.stream_settings.reality_settings.get("serverNames")[0]
        short_id = inbound.stream_settings.reality_settings.get("shortIds")[0]
        fp = inbound.stream_settings.reality_settings.get("settings", {}).get(
            "fingerprint", "chrome"
        )
        flow = client.flow

        connection_string = (
            f"vless://{client.id}@{self.vless_host}:{self.vless_port}"
            f"?type=tcp&security=reality&pbk={public_key}&fp={fp}&sni={website_name}"
            f"&sid={short_id}&spx=%2F"
        )
        if flow:
            connection_string += f"&flow={flow}"
        connection_string += f"#vless-{self.conventional_name}-{client.email}"

        return connection_string

    def __hash__(self) -> int:
        return hash((self.host, self.username, self.password, self.conventional_name))
