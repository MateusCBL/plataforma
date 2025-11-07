from datetime import datetime

class ItemVenda:
    def __init__(self, sell_id, product_id, quantity, created_at=None, updated_at=None):
        self.sell_id = sell_id
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()