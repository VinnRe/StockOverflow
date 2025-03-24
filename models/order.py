class Order:
    def __init__(self, order_content, order_date, order_status="Pending"):
        # Dictionary containing item names, quantities, and expiry dates
        self.order_content = order_content  
        
        # Date when the order was placed
        self.order_date = order_date  
        
        # Order status (default: Pending)
        self.order_status = order_status  

    def to_dict(self):
        # Convert object properties to a dictionary
        return {
            "order_content": self.order_content,
            "order_date": self.order_date,
            "order_status": self.order_status
        }