user_sessions = {}

def get_session(phone: str):
    return user_sessions.get(phone, {})

def update_session(phone: str, data: dict):
    user_sessions[phone] = {**get_session(phone), **data}

def clear_session(phone: str):
    if phone in user_sessions:
        del user_sessions[phone]