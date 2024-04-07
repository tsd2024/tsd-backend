import json

import redis
import threading

class RedisHandler:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.redis_client = redis.StrictRedis.from_url(connection_string)

    def upload_record(self, key, value):
        json_template = json.dumps(value)
        self.redis_client.set(key, json_template)

    def modify_record(self, key, field, new_value):
        pipe = self.redis_client.pipeline()
        while True:
            try:
                pipe.watch(key)
                current_value = pipe.hget(key, field)
                pipe.multi()
                pipe.hset(key, field, new_value)
                pipe.execute()
                break
            except redis.WatchError:
                continue
            finally:
                pipe.unwatch()

    def get_record(self, key):
        return self.redis_client.get(key)

