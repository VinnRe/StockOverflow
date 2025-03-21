class Order:
    def __init__(self, order_content, order_date, order_status="Pending"):
        self.order_content = order_content
        self.order_date = order_date
        self.order_status = order_status

    def to_dict(self):
        return {
            "order_content": self.order_content,
            "order_date": self.order_date,
            "order_status": self.order_status
        }