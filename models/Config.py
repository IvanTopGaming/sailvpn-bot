from pydantic import BaseModel


class Config(BaseModel):
    telegram_token: str
    telegram_logs_chat_id: int
    telegram_admins: list[int]

    @staticmethod
    def load_from_file(file_path: str):
        import json

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return Config.model_validate(data)
