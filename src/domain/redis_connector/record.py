
def get_redis_record_template():
    return {
        'lobby_metadata': {
            'max_players': 5,
            'admin_id': None,
            'number_of_rounds': 5,
            'round_number': 1,
            'available_cards': [1, 2, 3, 5, 8, 13, 21],
            'lobby_name': "",
        },
        'players': [
            {
                'player_id': None,
                'choose_cards': [],
                'choice_made': False,
            }
        ]
    }

def get_player_template():
    return {
        'player_id': None,
        'choose_cards': [],
        'choice_made': False,
    }
