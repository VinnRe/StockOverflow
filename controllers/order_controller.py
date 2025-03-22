import requests
import os
from dotenv import load_dotenv
from models.order import Order
from datetime import datetime

load_dotenv()
DB_URL = os.getenv("DB_URL") + "/orders.json"

class OrderController:
    def __init__(self):
        self.db_url = DB_URL

        # Placeholder inventory data (Simulating stock levels)
        self.inventory = {
            "Tomatoes": 5,
            "Cheese": 15,
            "Buns": 3,
            "Beef Patty": 8,
            "Lettuce": 20
        }

    def place_order(self, order: Order):
        """Places an order and saves it to Firebase (Placeholder for now)."""
        data = {
            "order_content": order.order_content,
            "order_date": order.order_date,
            "order_status": "Pending"
        }
        response = requests.post(self.db_url, json=data)
        if response.status_code == 200:
            print(f" Order placed successfully: {order.order_content}")
        else:
            print(" Failed to place order.")

    def get_all_orders(self):
        """Fetch all orders from Firebase."""
        response = requests.get(self.db_url)
        if response.status_code == 200 and response.json():
            return response.json()
        return {}

    def receive_order(self, order_id):
        """Updates an order status to 'Received'."""
        order_url = f"{self.db_url[:-5]}/{order_id}.json"
        response = requests.patch(order_url, json={"order_status": "Received"})
        if response.status_code == 200:
            print(" Order received successfully.")
        else:
            print(" Failed to update order status.")

    def check_ingredients(self):
        """
        Checks inventory stock levels.
        If any ingredient is below 10, it triggers auto_reorder().
        """
        print("\n🔍 Checking ingredient stock levels...")
        for item, qty in self.inventory.items():
            if qty < 10:
                print(f"\n⚠️ Low stock detected: {item} ({qty} left)")
                self.auto_reorder(item, qty)
        print("\n✅ Inventory check complete.")

    def auto_reorder(self, item, qty):
        """
        Automatically places an order for low-stock ingredients.
        Uses place_order() function to order.
        """
        order_quantity = 20 - qty
        order_content = {item: order_quantity}

        order = Order(order_content, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Place the order using place_order()
        self.place_order(order)