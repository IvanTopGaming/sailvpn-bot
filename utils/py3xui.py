from typing import List

from models.ClientSearchResult import ClientSearchResult


allowed_protocols = ["vless"]

async def find_client_by_uid(servers, uid) -> List[ClientSearchResult]:
    results = []
    for server in servers:
        async with server.new_session() as session:
            inbounds = await session.inbound.get_list()
            inbounds = [inbound for inbound in inbounds if inbound.protocol in allowed_protocols]
            for inbound in inbounds:
                print(f"Inbound: {inbound.remark} ({inbound.id})")
                for client in inbound.settings.clients:
                    print(f"\t{client.email}: {client.id}")
                    if client.id == "942ea5e5-daa6-439c-a987-d2229ed43460":
                        found_client = ClientSearchResult(
                            server=server,
                            inbound=inbound,
                            client=client
                        )
                        results.append(found_client)
    return results
