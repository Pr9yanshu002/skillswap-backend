import uuid

def create_meet_space() -> str:
    """
    Generates a unique Jitsi Meet room URL.
    No API, no auth, no cost — works immediately.
    """
    room = f"skillswap-{uuid.uuid4().hex[:12]}"
    return f"https://meet.jit.si/{room}"