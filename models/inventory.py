class InventoryItem:
    def __init__(self, itemName, stock):
        """
        :param itemName: Name of the inventory item
        :param stock: Dictionary where keys are expiry dates and values are quantities
                      Example: {"2025-06-19": 20, "2025-06-28": 30}
        """
        self.itemName = itemName
        self.stock = stock  # Expiry-date mapping
        self.totalQuantity = sum(stock.values())  # Calculate total quantity dynamically

    def to_dict(self):
        return {
            "itemName": self.itemName,
            "stock": self.stock,
            "totalQuantity": self.totalQuantity
        }