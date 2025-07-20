from pydantic import BaseModel


class AdditionalKey(BaseModel):
    name: str
    uuid: str
    preferred_server: str
