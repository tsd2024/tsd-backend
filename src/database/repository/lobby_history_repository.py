from pydantic import BaseModel

from src.database.database import SessionFactory
from src.database.model import DatabaseLobbyHistory


class LobbyHistoryRepository(BaseModel):
    session_factory: SessionFactory

    def add_or_update_lobby_history(self, lobby_id: str, player_id: str, lobby_metadata: str) -> None:
        with self.session_factory() as session:
            lobby_history = session.query(DatabaseLobbyHistory) \
                .filter((DatabaseLobbyHistory.lobby_id == lobby_id) & (DatabaseLobbyHistory.player_id == player_id)) \
                .first()
            if lobby_history:
                lobby_history.lobby_metadata = str(lobby_metadata)
            else:
                lobby_history = DatabaseLobbyHistory(lobby_id=lobby_id, player_id=player_id,
                                                     lobby_metadata=str(lobby_metadata))
                session.add(lobby_history)
            session.commit()

    def get_player_lobby_history(self, player_id: str) -> list:
        with self.session_factory() as session:
            result = session.query(DatabaseLobbyHistory) \
                .filter((DatabaseLobbyHistory.player_id == player_id)) \
                .all()
            return result
