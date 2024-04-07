from enum import Enum

from pydantic import BaseModel


class ActionType(Enum):
    CREATE = "create"
    JOIN = "join"




class Packet(BaseModel):
    action: ActionType
    value: dict