from enum import Enum

from pydantic import BaseModel


class ActionType(Enum):
    CREATE = "create"
    JOIN = "join"
    PLAY_CARD = "play_card"




class Packet(BaseModel):
    action: ActionType
    value: dict