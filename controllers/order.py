import requests
import os
from dotenv import load_dotenv
from models.order import Order

load_dotenv()
DB_URL = os.getenv("DB_URL") + "/orders.json"

class OrderController:
    def __init__(self):
        self.db_url = DB_URL

    def place_order(self, order: Order):
        data = {
            "order_content": order.order_content,
            "order_date": order.order_date,
            "order_status": "Pending"
        }
        response = requests.post(self.db_url, json=data)
        if response.status_code == 200:
            print("Order placed successfully.")
        else:
            print("Failed to place order.")

    def get_all_orders(self):
        response = requests.get(self.db_url)
        if response.status_code == 200 and response.json():
            return response.json()
        return {}

    def receive_order(self, order_id):
        order_url = f"{self.db_url[:-5]}/{order_id}.json"
        response = requests.patch(order_url, json={"order_status": "Received"})
        if response.status_code == 200:
            print("Order received successfully.")
        else:
            print("Failed to update order status.")
