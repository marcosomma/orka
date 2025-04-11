import redis
import json

class RedisQueue:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def publish(self, channel, message):
        self.redis.publish(channel, json.dumps(message))

    def subscribe(self, channel):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def push(self, queue_name, message):
        self.redis.rpush(queue_name, json.dumps(message))

    def pop(self, queue_name, block=True, timeout=5):
        if block:
            item = self.redis.blpop(queue_name, timeout=timeout)
        else:
            item = self.redis.lpop(queue_name)
        if item:
            _, data = item
            return json.loads(data)
        return None