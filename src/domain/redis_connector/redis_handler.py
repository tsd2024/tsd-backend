import json

import redis

from src.contract.exceptions import LobbyNotFoundException, CardNotAvailableException, PlayerNotFoundException, \
    RevealNotReadyException, NotAdminException, CancelNotAvailableException


class MaxPlayersReachedException(Exception):
    pass


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

                player_ids = [player['player_id'] for player in players]
                if player_id in player_ids:
                    return lobby_data

                if len(players) >= max_players:
                    raise MaxPlayersReachedException("Lobby is full")
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

    def reveal_cards(self, lobby_key, player_id):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                admin_id = lobby_data['lobby_metadata']['admin_id']
                if player_id != admin_id:
                    raise NotAdminException("Only admin can reveal cards")
                players = lobby_data['players']
                all_choices_made = all(player['choice_made'] for player in players)
                if all_choices_made:
                    lobby_data['lobby_metadata']['reveal_cards'] = True
                    pipe.multi()
                    pipe.set(lobby_key, json.dumps(lobby_data))
                    pipe.execute()
                    return lobby_data
                else:
                    raise RevealNotReadyException("Not all players have made their choice")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def get_lobby_status(self, lobby_key):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                reveal_cards = lobby_data['lobby_metadata'].get('reveal_cards', False)
                players = lobby_data['players']

                num_players = len(players)

                round_number = lobby_data['lobby_metadata']['round_number']

                game_status = {
                    'num_players': num_players,
                    'reveal_ready': reveal_cards,
                    'round_number': round_number,
                    'players': []
                }

                for player in players:
                    if reveal_cards:
                        player_info = {
                            'player_id': player['player_id'],
                            'card': player['choose_cards'][-1],
                            'ready': True
                        }
                    else:
                        player_info = {
                            'player_id': player['player_id'],
                            'card': None,
                            'ready': True if player['choice_made'] else False
                        }
                    game_status['players'].append(player_info)

                return game_status
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def cancel_choice(self, lobby_key, player_id):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                players = lobby_data['players']
                reveal_cards = lobby_data['lobby_metadata'].get('reveal_cards', False)

                for player in players:
                    if player['player_id'] == player_id:
                        if player['choice_made'] and not reveal_cards:
                            player['choice_made'] = False
                            pipe.multi()
                            pipe.set(lobby_key, json.dumps(lobby_data))
                            pipe.execute()
                            return True
                        else:
                            raise CancelNotAvailableException("Cancellation not allowed under current conditions")

                raise PlayerNotFoundException("Player not found in the lobby")

            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def get_record(self, key):
        return self.redis_client.get(key)
