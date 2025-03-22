class Order:
    def __init__(self, order_content, order_date, order_status="Pending"):
        """
        order_content should be a dictionary where each key is an item name, 
        and its value is another dictionary with 'quantity' and 'expiry_date'.
        Example:
        {
            "Tomatoes": {"quantity": 10, "expiry_date": "2025-04-10"},
            "Onions": {"quantity": 5, "expiry_date": "2025-03-30"}
        }
        """
        self.order_content = order_content
        self.order_date = order_date
        self.order_status = order_status

    def to_dict(self):
        return {
            "order_content": self.order_content,
            "order_date": self.order_date,
            "order_status": self.order_status
        }
