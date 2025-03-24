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
        # Set database URL and initialize inventory controller
        self.db_url = DB_URL
        self.inventory = FoodInventory()

    def place_order(self, order: Order):
        # Save the order to Firebase
        data = order.to_dict()
        response = requests.post(self.db_url, json=data)
        if response.status_code == 200:
            print(f"Order placed successfully: {order.order_content}")
        else:
            print("Failed to place order.")

    def get_all_orders(self):
        # Fetch all orders from Firebase
        response = requests.get(self.db_url)
        if response.status_code == 200 and response.json():
            return response.json()
        return {}

    def receive_order(self, order_id):
        # Mark an order as received and update inventory
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

            # Mark order as received in the database
            requests.patch(order_url, json={"order_status": "Received"})
            print(f"Order {order_id} received and inventory updated.")
        else:
            print("Failed to fetch order data.")
