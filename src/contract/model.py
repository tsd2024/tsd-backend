import uuid
from enum import Enum

from pydantic import BaseModel


class ActionType(Enum):
    CREATE = "create"
    JOIN = "join"
    PLAY_CARD = "play_card"
    REVEAL = "reveal"
    CANCEL = "cancel"
    NEXT_ROUND = "next_round"


class Packet(BaseModel):
    action: ActionType
    value: dict


class Player(BaseModel):
    player_id: str
    lobby_key: str


class BasicLobbyInfo(BaseModel):
    lobby_id: str
    lobby_name: str
    admin_id: str


class Ticket(BaseModel):
    ticket_name: str


class Story(BaseModel):
    story_id: str
    story_name: str
    story_points: int
    tickets: list[Ticket]
