import json, redis
from ..config import settings

try:
    _r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    _r.ping()
except Exception:
    _r = None

def cached(key: str, ttl: int, fn):
    if _r:
        hit = _r.get(key)
        if hit:
            return json.loads(hit)
    val = fn()
    if _r:
        _r.setex(key, ttl, json.dumps(val, default=str))
    return val

def invalidate(user_id: int):
    if _r:
        for k in _r.scan_iter(f"u{user_id}:*"):
            _r.delete(k)
