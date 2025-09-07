from typing import Optional, List

from pydantic import BaseModel, Field

from models.AdditionalKey import AdditionalKey


class User(BaseModel):
    uuid: str
    tgid: int
    readable_name: str
    preferred_server: str

    # Используем alias для поля с пробелом в имени
    endless_premium: Optional[bool] = Field(None, alias="endless premium")

    # Эти поля могут отсутствовать в JSON, поэтому они опциональные
    referer: Optional[str] = None
    additional_keys: Optional[List[AdditionalKey]] = None
