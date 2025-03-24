class InventoryItem:
    def __init__(self, itemName, stock):
        # Initialize item name and stock with expiry-date mapping
        self.itemName = itemName
        self.stock = stock  
        
        # Calculate total quantity based on stock values
        self.totalQuantity = sum(stock.values())

    def to_dict(self):
        # Convert object properties to a dictionary
        return {
            "itemName": self.itemName,
            "stock": self.stock,
            "totalQuantity": self.totalQuantity
        }
