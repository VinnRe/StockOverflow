from models.inventory import InventoryItem
from firebase_admin import db
from datetime import datetime, timedelta

class FoodInventory:
    def __init__(self):
        # Initialize database references
        self.ref = db.reference('db')
        self.items_ref = self.ref.child('inventory')

    def displayItems(self, sortBy="itemName", isReversed=False):
        current_date = datetime.now().date()
        warning_date = current_date + timedelta(days=7)

        # Retrieve all items from the database
        items = self.items_ref.get()
        if not items:
            print("No items found in inventory.")
            return []
        
        inventory_list = []

        for item_id, item_data in items.items():
            is_low = False
            near_expiry = False
            
            # Check if any item is near expiry
            expiry_date_str = item_data.get("stock")
            if expiry_date_str:
                for item_expiry_date in expiry_date_str.keys():
                    expiry_date = datetime.strptime(item_expiry_date, "%Y-%m-%d").date()
                    if expiry_date < warning_date:
                        near_expiry = True

            # Check if item stock is low
            item_stock = item_data.get("totalQuantity")
            if item_stock < 20:
                is_low = True

            item_data["is_low"] = is_low
            item_data["near_expiry"] = near_expiry
            inventory_list.append({item_id: item_data})

        # Sort the inventory list based on the given criteria
        if sortBy == "itemName":
            inventory_list.sort(key=lambda x: list(x.values())[0]["itemName"])
        elif sortBy == "stock":
            inventory_list.sort(key=lambda x: min(list(x.values())[0]["stock"].keys()))
        elif sortBy == "totalQuantity":
            inventory_list.sort(key=lambda x: list(x.values())[0]["totalQuantity"])

        if isReversed:
            inventory_list.reverse()

        return inventory_list

    # Admin Functions
    def createItem(self, item):
        # Add a new item or update stock if it already exists
        try:
            itemName = item["itemName"]
            new_stock = item["stock"] 

            # Check if item already exists
            existing_items = self.items_ref.order_by_child("itemName").equal_to(itemName).get()

            if existing_items:
                # If the item exists, update its stock
                for item_id, existing_item in existing_items.items():
                    existing_stock = existing_item.get("stock", {})

                    # Add new quantities to existing stock
                    for expiry_date, quantity in new_stock.items():
                        existing_stock[expiry_date] = existing_stock.get(expiry_date, 0) + quantity

                    totalQuantity = sum(existing_stock.values())

                    self.items_ref.child(item_id).update({
                        "stock": existing_stock,
                        "totalQuantity": totalQuantity
                    })
                    print(f"Updated stock for {itemName}. New total: {totalQuantity}")
                    return {item_id: {"itemName": itemName, "stock": existing_stock, "totalQuantity": totalQuantity}}

            else:
                # Create a new item if it doesn't exist
                new_item = InventoryItem(itemName, new_stock)
                new_item_dict = new_item.to_dict()
                new_ref = self.items_ref.push(new_item_dict)
                print(f"Created new item: {itemName}")
                return {new_ref.key: new_item}

        except Exception as e:
            print(f"Error creating/updating item: {e}")
            return None

    def updateItem(self, itemId, item):
        # Update an existing item and recalculate total quantity if stock is modified
        try:
            if "stock" in item:
                item["totalQuantity"] = sum(item["stock"].values())

            self.items_ref.child(itemId).update(item)
            print(f"Updated item: {itemId}")
        except Exception as e:
            print(f"Error updating item: {e}")

    def deleteItem(self, itemId):
        # Remove an item from the inventory
        try:
            self.items_ref.child(itemId).delete()
            print(f"Deleted item: {itemId}")
        except Exception as e:
            print(f"Error deleting item: {e}")
