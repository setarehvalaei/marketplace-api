class Order:
    def __init__(self, id, items, shipping_address, total, status):
        self.id = id
        self.items = items
        self.shipping_address = shipping_address
        self.total = total
        self.status = status