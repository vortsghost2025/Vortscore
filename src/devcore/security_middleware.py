class TokenValidator:
    def __init__(self):
        self.authorized_tokens = ["VITALIS_SUPERUSER_2026"]

    def validate_request(self, token: str) -> bool:
        return token in self.authorized_tokens
