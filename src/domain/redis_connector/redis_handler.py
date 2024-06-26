import json
import statistics
import redis

from src.contract.exceptions import LobbyNotFoundException, CardNotAvailableException, PlayerNotFoundException, \
    RevealNotReadyException, NotAdminException, CancelNotAvailableException, NextRoundNotReadyException, \
    MaxRoundsReachedException, MaxUserStoriesReachedException, UserStoryNotFoundException


class MaxPlayersReachedException(Exception):
    pass


class RedisHandler:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.redis_client = redis.StrictRedis.from_url(connection_string)

    def upload_record(self, key, value):
        json_template = json.dumps(value)
        self.redis_client.set(key, json_template)

    def join_lobby(self, lobby_key, player_id, player_name):
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
                    'player_name': player_name,
                    'choose_cards': [],
                    'choice_made': False,
                    'round_number': 1
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
                    latest_cards = [player['choose_cards'][-1] for player in players]
                    average_card = statistics.median(latest_cards)

                    lobby_data['lobby_metadata']['results'].append(average_card)

                    round_number = lobby_data['lobby_metadata']['round_number']
                    user_stories = lobby_data.get('user_stories', [])

                    if round_number <= len(user_stories):
                        user_stories[round_number - 1]['story_points'] = int(average_card)

                    lobby_data['user_stories'] = user_stories

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
                user_stories = lobby_data.get('user_stories', [])
                number_of_rounds = lobby_data['lobby_metadata']['number_of_rounds']
                round_number = lobby_data['lobby_metadata']['round_number']

                num_players = len(players)

                current_user_story_id = None
                if user_stories and round_number <= len(user_stories):
                    current_user_story_id = user_stories[round_number - 1]['story_id'] if user_stories else None

                game_status = {
                    'num_players': num_players,
                    'reveal_ready': reveal_cards,
                    'round_number': round_number,
                    'number_of_rounds': number_of_rounds,
                    'current_user_story_id': current_user_story_id,
                    'players': [],
                    'user_stories': user_stories,
                    "admin_id": lobby_data['lobby_metadata']['admin_id']
                }

                for player in players:
                    if reveal_cards:
                        player_info = {
                            'player_id': player['player_id'],
                            'player_name': player['player_name'],
                            'card': player['choose_cards'][-1],
                            'ready': True
                        }
                    else:
                        player_info = {
                            'player_id': player['player_id'],
                            'player_name': player['player_name'],
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

    def next_round(self, lobby_key, player_id):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                admin_id = lobby_data['lobby_metadata']['admin_id']
                reveal_cards = lobby_data['lobby_metadata']['reveal_cards']
                round_number = lobby_data['lobby_metadata']['round_number']
                max_rounds = lobby_data['lobby_metadata']['number_of_rounds']
                if player_id != admin_id:
                    raise NotAdminException("Only admin can start next round")
                players = lobby_data['players']
                all_choices_made = all(player['choice_made'] for player in players)
                if all_choices_made and reveal_cards and round_number < max_rounds:
                    # Increase round number
                    lobby_data['lobby_metadata']['round_number'] += 1
                    # Set reveal_cards to False
                    lobby_data['lobby_metadata']['reveal_cards'] = False
                    # Reset choice_made for each player
                    for player in players:
                        player['choice_made'] = False
                    pipe.multi()
                    pipe.set(lobby_key, json.dumps(lobby_data))
                    pipe.execute()
                    return lobby_data
                else:
                    if round_number >= max_rounds:
                        raise MaxRoundsReachedException("All rounds have been played")
                    else:
                        raise NextRoundNotReadyException("Not all players have made their choice")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def add_user_story(self, lobby_key, user_story):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                max_rounds = lobby_data['lobby_metadata']['number_of_rounds']
                user_stories = lobby_data.get('user_stories', [])
                if len(user_stories) < max_rounds:
                    user_stories.append(user_story)
                    lobby_data['user_stories'] = user_stories
                    pipe.multi()
                    pipe.set(lobby_key, json.dumps(lobby_data))
                    pipe.execute()
                    return lobby_data
                else:
                    raise MaxUserStoriesReachedException("Maximum user stories reached")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def update_user_story(self, lobby_key, updated_story):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                user_stories = lobby_data.get('user_stories', [])
                for user_story in user_stories:
                    if user_story['story_id'] == updated_story['story_id']:
                        user_story.update(updated_story)
                        pipe.multi()
                        pipe.set(lobby_key, json.dumps(lobby_data))
                        pipe.execute()
                        return lobby_data
                raise UserStoryNotFoundException(f"User story with ID {updated_story['story_id']} not found")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def delete_user_story(self, lobby_key, story_id):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                user_stories = lobby_data.get('user_stories', [])
                for user_story in user_stories:
                    if user_story['story_id'] == story_id:
                        user_stories.remove(user_story)
                        pipe.multi()
                        pipe.set(lobby_key, json.dumps(lobby_data))
                        pipe.execute()
                        return lobby_data
                raise UserStoryNotFoundException(f"User story with ID {story_id} not found")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def sync_player_round_number(self, lobby_key, player_id):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(lobby_key)
                lobby_data = pipe.get(lobby_key)
                if not lobby_data:
                    raise LobbyNotFoundException("Lobby not found")
                lobby_data = json.loads(lobby_data.decode())
                lobby_round_number = lobby_data['lobby_metadata']['round_number']
                admin_id = lobby_data['lobby_metadata']['admin_id']
                players = lobby_data['players']
                for player in players:
                    if player['player_id'] == player_id and player_id != admin_id:
                        player_round_number = player.get('round_number', 1)
                        if lobby_round_number > player_round_number:
                            player['round_number'] = lobby_round_number
                            pipe.multi()
                            pipe.set(lobby_key, json.dumps(lobby_data))
                            pipe.execute()
                            return True
                        else:
                            return False
                raise PlayerNotFoundException(f"Player with ID {player_id} not found in the lobby")
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def get_record(self, key):
        return self.redis_client.get(key)
