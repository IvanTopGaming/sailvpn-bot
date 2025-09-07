from models.User import User


class LoggingService:
    def __init__(self, app):
        self.app = app

    async def on_service_start(self):
        print("Logging service started")
        await self.app.tglogger.log("✅ Starting bot")

    async def on_user_request_keys(self, user: User):
        print("User requested keys:", user.readable_name, user.uuid)
        await self.app.tglogger.log(
            f"🔑 User {user.readable_name} ({user.uuid}) requested keys."
        )

    async def on_user_request_statistics(self, user: User):
        print("User requested statistics:", user.readable_name, user.uuid)
        await self.app.tglogger.log(
            f"📊 User {user.readable_name} ({user.uuid}) requested statistics."
        )
