from enum import Enum

from pydantic import BaseModel


class ActionType(Enum):
    CREATE = "create"
    JOIN = "join"
    PLAY_CARD = "play_card"
    REVEAL = "reveal"


class Packet(BaseModel):
    action: ActionType
    value: dict


class Player(BaseModel):
    player_id: str
    lobby_key: str
