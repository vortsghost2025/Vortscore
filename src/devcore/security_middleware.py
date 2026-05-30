import os

class SecurityMiddleware:
    def __init__(self):
        # Load from environment — never hardcode
        token = os.environ.get("VITALIS_SUPERUSER_TOKEN")
        self.authorized_tokens = [token] if token else []
        if not token:
            print("[SECURITY] WARNING: VITALIS_SUPERUSER_TOKEN not set in environment")

    def is_authorized(self, token):
        return token in self.authorized_tokens
