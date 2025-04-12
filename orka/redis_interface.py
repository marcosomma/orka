# OrKa: Orchestrator Kit Agents
# Copyright © 2025 Marco Somma
#
# This file is part of OrKa – https://github.com/marcosomma/orka
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes without explicit permission.
#
# Full license: https://creativecommons.org/licenses/by-nc/4.0/legalcode
# For commercial use, contact: marcosomma.work@gm
# 
# Required attribution: OrKa by Marco Somma – https://github.com/marcosomma/orka

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