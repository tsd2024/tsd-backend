import json

import redis
import threading

from src.contract.exceptions import LobbyNotFoundException, CardNotAvailableException, PlayerNotFoundException


class RedisHandler:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.redis_client = redis.StrictRedis.from_url(connection_string)

    def upload_record(self, key, value):
        json_template = json.dumps(value)
        self.redis_client.set(key, json_template)


    def join_lobby(self, lobby_key, player_id):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                max_players = lobby_data['lobby_metadata']['max_players']
                players = lobby_data['players']
                if len(players) >= max_players:
                    raise ValueError("Lobby is full")
                players.append({
                    'player_id': player_id,
                    'choose_cards': [],
                    'choice_made': False,
                })
                pipe.multi()
                pipe.set(lobby_key, json.dumps(lobby_data))
                pipe.execute()
                return lobby_data
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def play_card(self, lobby_key, player_id, card):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())  # Convert JSON to dictionary
                players = lobby_data['players']
                for player in players:
                    if player['player_id'] == player_id:
                        if card not in lobby_data['lobby_metadata']['available_cards']:
                            raise CardNotAvailableException("Card not in available cards")
                        player['choose_cards'].append(card)
                        player['choice_made'] = True
                        pipe.multi()
                        pipe.set(lobby_key, json.dumps(lobby_data))
                        pipe.execute()
                        return lobby_data
                raise PlayerNotFoundException("Player not found")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def get_record(self, key):
        return self.redis_client.get(key)

