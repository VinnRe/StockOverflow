import requests
import os
from dotenv import load_dotenv
from models.order import Order
from datetime import datetime
from controllers.food_inventory_controller import FoodInventory

load_dotenv()
DB_URL = os.getenv("DB_URL") + "/orders.json"

class OrderController:
    def __init__(self):
        self.db_url = DB_URL
        self.inventory = FoodInventory()

    def place_order(self, order: Order):
        """Places an order and saves it to Firebase."""
        data = order.to_dict()
        response = requests.post(self.db_url, json=data)
        if response.status_code == 200:
            print(f"Order placed successfully: {order.order_content}")
        else:
            print("Failed to place order.")

    def get_all_orders(self):
        """Fetch all orders from Firebase."""
        response = requests.get(self.db_url)
        if response.status_code == 200 and response.json():
            return response.json()
        return {}

    def receive_order(self, order_id):
        """Marks an order as received and updates inventory accordingly."""
        order_url = f"{self.db_url[:-5]}/{order_id}.json"
        response = requests.get(order_url)
        
        if response.status_code == 200 and response.json():
            order_data = response.json()
            order_content = order_data.get("order_content", {})

            # Update inventory with received items and their respective expiry dates
            for item_name, item_details in order_content.items():
                quantity = item_details["quantity"]
                expiry_date = item_details["expiry_date"]

                self.inventory.createItem({
                    "itemName": item_name,
                    "stock": {expiry_date: quantity}
                })

            # Mark order as received
            requests.patch(order_url, json={"order_status": "Received"})
            print(f"Order {order_id} received and inventory updated.")
        else:
            print("Failed to fetch order data.")

    def check_ingredients(self):
        """
        Checks inventory stock levels.
        If any ingredient is below 10, it triggers auto_reorder().
        """
        print("\nChecking ingredient stock levels...")
        inventory_data = self.inventory.get_all_items()  # Fetch inventory items

        for item_name, item_data in inventory_data.items():
            total_qty = item_data.get("totalQuantity", 0)
            if total_qty < 10:
                print(f"\nLow stock detected: {item_name} ({total_qty} left)")
                self.auto_reorder(item_name, total_qty)
        
        print("\nInventory check complete.")

    def auto_reorder(self, item, qty):
        """
        Automatically places an order for low-stock ingredients.
        Uses place_order() function to order.
        """
        order_quantity = 20 - qty
        expiry_date = input(f"Enter expiry date for reordered {item} (YYYY-MM-DD): ").strip()
        
        order_content = {item: {"quantity": order_quantity, "expiry_date": expiry_date}}
        order = Order(order_content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Place the order using place_order()
        self.place_order(order)