import os
import json
import redis
from datetime import datetime

class RedisMemoryLogger:

    def __init__(self, redis_url=None, stream_key="orka:memory"):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.stream_key = stream_key
        self.client = redis.from_url(self.redis_url)
        self.memory = []  # 🧠 Local memory buffer

    def log(self, agent_id, event_type, payload):
        event = {
            "agent_id": agent_id,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload  # <-- keep as dict here
        }
        self.memory.append(event)

        # Safe encoding for Redis
        self.client.xadd(self.stream_key, {
            "agent_id": agent_id,
            "event_type": event_type,
            "timestamp": event["timestamp"],
            "payload": json.dumps(payload)  # <- just here for Redis compatibility
        })

    def save_to_file(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
        print(f"[MemoryLogger] Logs saved to {file_path}")

    def tail(self, count=10):
        return self.client.xrevrange(self.stream_key, count=count)


# Future stub
class KafkaMemoryLogger:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Kafka backend not implemented yet")