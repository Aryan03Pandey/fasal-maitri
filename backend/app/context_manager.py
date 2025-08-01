import os
import json
import redis
from typing import List, Dict

# Load from env or config
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_TTL = int(os.getenv("SESSION_TTL", 3600))  # optional expiration
MAX_PER_USER_BYTES = 2 * 1024 * 1024  # 2MB

r = redis.from_url(REDIS_URL, decode_responses=True)  # strings

def _history_key(session_id: str) -> str:
    return f"session:{session_id}:history"

def _size_key(session_id: str) -> str:
    return f"session:{session_id}:size"

def append_message(session_id: str, role: str, text: str):
    """
    Appends a message (role: "user" or "assistant") to the session history.
    Evicts oldest entries if total serialized size exceeds limit.
    """
    key = _history_key(session_id)
    size_key = _size_key(session_id)

    entry = {"role": role, "text": text}
    entry_json = json.dumps(entry, ensure_ascii=False)
    entry_bytes = entry_json.encode("utf-8")
    entry_size = len(entry_bytes)

    # Push new entry to right
    r.rpush(key, entry_json)
    # Update running size
    current_size = r.get(size_key)
    current_size = int(current_size) if current_size else 0
    new_size = current_size + entry_size
    r.set(size_key, new_size)
    r.expire(key, SESSION_TTL)
    r.expire(size_key, SESSION_TTL)

    # Evict oldest until under limit
    while new_size > MAX_PER_USER_BYTES:
        oldest = r.lpop(key)
        if not oldest:
            break
        try:
            oldest_entry = oldest.encode("utf-8")
            oldest_size = len(oldest_entry)
        except Exception:
            oldest_size = 0
        new_size -= oldest_size
        if new_size < 0:
            new_size = 0
        r.set(size_key, new_size)
        r.expire(key, SESSION_TTL)
        r.expire(size_key, SESSION_TTL)

def get_recent(session_id: str, limit: int = 5) -> List[Dict]:
    """
    Returns the last `limit` messages as list of dicts with keys 'role' and 'text'.
    """
    key = _history_key(session_id)
    raw = r.lrange(key, -limit, -1) or []
    return [json.loads(item) for item in raw]

def get_full_history(session_id: str) -> List[Dict]:
    key = _history_key(session_id)
    raw = r.lrange(key, 0, -1) or []
    return [json.loads(item) for item in raw]

def clear_history(session_id: str):
    r.delete(_history_key(session_id))
    r.delete(_size_key(session_id))
