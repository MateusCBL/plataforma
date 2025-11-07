from datetime import datetime

class Cotacao:
    def __init__(self, code, value, created_at=None):
        self.code = code
        self.value = value
        self.created_at = created_at or datetime.utcnow()