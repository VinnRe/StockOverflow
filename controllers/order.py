import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OrderController:
    def __init__(self):
        self.db_url = os.getenv("DB_URL") + "/orders.json"

    def place_order(self, order):
        order_data = {
            "order_content": order.order_content,
            "order_date": order.order_date,
            "order_status": "Pending"
        }
        response = requests.post(self.db_url, json=order_data)
        if response.status_code == 200:
            print("Order placed successfully.")
        else:
            print("Failed to place order.")

    def receive_order(self, order_id):
        update_url = os.getenv("DB_URL") + f"/orders/{order_id}.json"
        response = requests.patch(update_url, json={"order_status": "Received"})
        if response.status_code == 200:
            print("Order received successfully.")
        else:
            print("Failed to update order status.")
