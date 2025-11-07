from datetime import datetime

class Venda:
    def __init__(self, id, client_id, status=0, created_at=None, updated_at=None):
        self.id = id
        self.client_id = client_id
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()