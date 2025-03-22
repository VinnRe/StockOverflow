from firebase_admin import db
from datetime import datetime, timedelta

class FoodInventory:
    def __init__(self):
        self.ref = db.reference('db')
        self.items_ref = self.ref.child('inventory')

    def displayItems(self):
        """Retrieve and display all inventory items."""
        current_date = datetime.now().date()
        warning_date = current_date + timedelta(days=7)

        items = self.items_ref.get()
        if not items:
            print("No items found in inventory.")
            return []
        
        inventory_list = []
        items_near_expiry_date = {}
        item_low_stock = []

        for item_id, item_data in items.items():
            inventory_list.append({item_id: item_data})

            expiry_date_str = item_data.get("stock")
            if expiry_date_str:
                for item_expiry_date, item_quantity in expiry_date_str.items():
                    print(item_expiry_date)
                    expiry_date = datetime.strptime(item_expiry_date, "%Y-%m-%d").date()
                    if expiry_date < warning_date:
                        print(items_near_expiry_date.get(item_id))
                        if not items_near_expiry_date.get(item_id):
                            items_near_expiry_date[item_id] = {
                                'itemName': item_data['itemName'],
                                'stock': {item_expiry_date: item_quantity}
                            }
                        else:
                            items_near_expiry_date[item_id]['stock'][item_expiry_date] = item_quantity

            item_stock = item_data.get("totalQuantity")
            if item_stock < 20:
                item_low_stock.append({item_id: item_data})

        print(f"inventory_list: {inventory_list}")
        print()
        print(f"items_near_expiry_date: {items_near_expiry_date}")
        print()
        print(f"item_low_stock: {item_low_stock}")
        
        return inventory_list

    def searchItemById(self, itemId):
        """Search for an item by its Firebase ID."""
        try:
            item = self.items_ref.child(itemId).get()
            if not item:
                print(f"No item found with ID: {itemId}")
                return None
            return {itemId: item}
        except Exception as e:
            print(f"Error searching for item by ID: {e}")
            return None

    def searchItemByName(self, itemName):
        """Search for an item by its name."""
        try:
            items = self.items_ref.order_by_child("itemName").equal_to(itemName).get()
            if not items:
                print(f"No item found with name: {itemName}")
                return None
            
            result = {}
            for item_id, item_data in items.items():
                result[item_id] = item_data
            
            return result
        except Exception as e:
            print(f"Error searching for item by name: {e}")
            return None

    def changeQuantity(self, itemId, expiryDate, quantity):
        """
        Update quantity of an item based on expiry date.
        If expiryDate exists, update quantity; otherwise, add a new entry.
        Also updates the total quantity.
        """
        try:
            item = self.items_ref.child(itemId).get()
            if not item:
                print(f"No item found with ID: {itemId}")
                return
            
            stock = item.get("stock", {})

            # If expiry date exists, update its quantity
            stock[expiryDate] = stock.get(expiryDate, 0) + quantity

            # Update total quantity
            totalQuantity = sum(stock.values())

            self.items_ref.child(itemId).update({
                "stock": stock,
                "totalQuantity": totalQuantity
            })
            print(f"Updated quantity for {item['itemName']} (Expiry: {expiryDate}) to {stock[expiryDate]}.")
        except Exception as e:
            print(f"Error updating quantity: {e}")

    # Admin Functions
    def createItem(self, item):
        """
        Adds a new item or updates an existing one.
        - If the item exists, updates its stock instead of creating a new entry.
        - If the expiry date exists, adds to its quantity instead of overwriting.
        """
        try:
            itemName = item["itemName"]
            new_stock = item["stock"] 

            # Check if item already exists
            existing_items = self.items_ref.order_by_child("itemName").equal_to(itemName).get()

            if existing_items:
                # If the item exists, update the existing stock
                for item_id, existing_item in existing_items.items():
                    existing_stock = existing_item.get("stock", {})

                    for expiry_date, quantity in new_stock.items():
                        if expiry_date in existing_stock:
                            existing_stock[expiry_date] += quantity
                        else:
                            existing_stock[expiry_date] = quantity

                    totalQuantity = sum(existing_stock.values())

                    self.items_ref.child(item_id).update({
                        "stock": existing_stock,
                        "totalQuantity": totalQuantity
                    })
                    print(f"Updated stock for {itemName}. New total: {totalQuantity}")
                    return {item_id: {"itemName": itemName, "stock": existing_stock, "totalQuantity": totalQuantity}}

            else:
                # If item doesn't exist, create a new entry
                totalQuantity = sum(new_stock.values())
                new_item = {
                    "itemName": itemName,
                    "stock": new_stock,
                    "totalQuantity": totalQuantity
                }
                new_ref = self.items_ref.push(new_item)
                print(f"Created new item: {itemName}")
                return {new_ref.key: new_item}

        except Exception as e:
            print(f"Error creating/updating item: {e}")
            return None

    def updateItem(self, itemId, item):
        """Update an existing inventory item, ensuring total quantity stays updated."""
        try:
            if "stock" in item:
                item["totalQuantity"] = sum(item["stock"].values())

            self.items_ref.child(itemId).update(item)
            print(f"Updated item: {itemId}")
        except Exception as e:
            print(f"Error updating item: {e}")

    def deleteItem(self, itemId):
        """Delete an item from inventory."""
        try:
            self.items_ref.child(itemId).delete()
            print(f"Deleted item: {itemId}")
        except Exception as e:
            print(f"Error deleting item: {e}")