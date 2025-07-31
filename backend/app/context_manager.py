import redis
import json
from .config import settings

r = redis.from_url(settings.redis_url, decode_responses=True)

def append_message(session_id: str, role: str, text: str):
    key = f"session:{session_id}:history"
    entry = json.dumps({"role": role, "text": text})
    r.rpush(key, entry)
    r.expire(key, settings.session_ttl)

def get_recent(session_id: str, limit=3):
    key = f"session:{session_id}:history"
    entries = r.lrange(key, -limit, -1)
    return [json.loads(e) for e in entries]
