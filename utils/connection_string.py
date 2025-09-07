from py3xui import Inbound


def get_connection_string(
    inbound: Inbound,
    user_uuid: str,
    server_host: str,
    server_port: int,
    user_name: str,
    server_name: str,
) -> str:
    """Prepare a connection string for the given inbound, user UUID and telegram ID.

    Arguments:
        inbound (Inbound): The inbound object.
        user_uuid (str): The UUID of the user.
        server_host (str): The host of the server.
        server_port (int): The port of the server.

    Returns:
        str: The connection string.
    """
    public_key = inbound.stream_settings.reality_settings.get("settings").get(
        "publicKey"
    )
    website_name = inbound.stream_settings.reality_settings.get("serverNames")[0]
    short_id = inbound.stream_settings.reality_settings.get("shortIds")[0]
    fp = inbound.stream_settings.reality_settings.get("settings", {}).get(
        "fingerprint", "chrome"
    )
    flow = inbound.stream_settings.reality_settings.get("settings", {}).get(
        "flow", "xtls-rprx-vision"
    )

    connection_string = (
        f"vless://{user_uuid}@{server_host}:{server_port}"
        f"?type=tcp&security=reality&pbk={public_key}&fp={fp}&sni={website_name}"
        f"&sid={short_id}&spx=%2F"
    )
    if flow:
        connection_string += f"&flow={flow}"
    connection_string += f"#vless-{server_name}-{user_name}"

    return connection_string
