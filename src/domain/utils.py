import random


def generate_unique_id():
    return '-'.join(str(random.randint(100, 999)) for _ in range(2))