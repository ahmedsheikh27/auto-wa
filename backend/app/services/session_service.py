import json
from app.core.redis import redis_client

SESSION_TTL = 1800 

def save_session(customer_phone, data):

    redis_client.setex(
        f"session:{customer_phone}",
        SESSION_TTL,
        json.dumps(data)
    )

def get_session(customer_phone):

    data = redis_client.get(f"session:{customer_phone}")

    if not data:
        return None

    return json.loads(data)

def clear_session(customer_phone):

    redis_client.delete(f"session:{customer_phone}")