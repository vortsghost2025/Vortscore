import uuid

def record(prompt, answer, confidence, tags=None):
    entry_id = str(uuid.uuid4())[:8]
    return entry_id
