import os
import sys

from data.repository.UsersRepository import UsersRepository


async def main():
    file = sys.argv[1] if len(sys.argv) > 1 else "users.json"
    users_repo = UsersRepository(file=file)
    users = users_repo.list_users()
    clients_to_create = [{"uuid": user.uuid, "name": user.readable_name, "server": user.preferred_server} for user in users]
    for user in users:
        for additional_key in user.additional_keys or []:
            clients_to_create.append({
                "uuid": additional_key.uuid,
                "name": additional_key.name,
                "server": additional_key.preferred_server
            })

    print("Loaded", len(clients_to_create), "clients to create from", file)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
