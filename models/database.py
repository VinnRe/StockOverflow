"""
Database interaction class for StockOverflow
"""

import os
import json
from datetime import datetime, timedelta

class Database:
    """Mock database class for storing and retrieving data"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        # Create sample data files if they don't exist
        self._create_sample_data()
    
    def _create_sample_data(self):
        """Create sample data files if they don't exist"""
        
        # Sample inventory items
        inventory_file = os.path.join(self.data_dir, "inventory.json")
        if not os.path.exists(inventory_file):
            sample_inventory = [
                {"id": 1, "name": "Tomatoes", "quantity": 20, "unit": "kg", "expiry": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), "category": "Vegetables"},
                {"id": 2, "name": "Chicken Breast", "quantity": 15, "unit": "kg", "expiry": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"), "category": "Meat"},
                {"id": 3, "name": "Olive Oil", "quantity": 5, "unit": "L", "expiry": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"), "category": "Oils"},
                {"id": 4, "name": "Flour", "quantity": 25, "unit": "kg", "expiry": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"), "category": "Dry Goods"},
                {"id": 5, "name": "Milk", "quantity": 10, "unit": "L", "expiry": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"), "category": "Dairy"}
            ]
            with open(inventory_file, 'w') as f:
                json.dump(sample_inventory, f, indent=4)
        
        # Sample recipes
        recipes_file = os.path.join(self.data_dir, "recipes.json")
        if not os.path.exists(recipes_file):
            sample_recipes = [
                {
                    "id": 1, 
                    "name": "Tomato Soup", 
                    "ingredients": [
                        {"item_id": 1, "quantity": 2, "unit": "kg"},
                        {"item_id": 3, "quantity": 0.1, "unit": "L"}
                    ],
                    "cost": 12.50,
                    "category": "Soups"
                },
                {
                    "id": 2, 
                    "name": "Chicken Pasta", 
                    "ingredients": [
                        {"item_id": 2, "quantity": 0.5, "unit": "kg"},
                        {"item_id": 4, "quantity": 0.3, "unit": "kg"},
                        {"item_id": 3, "quantity": 0.05, "unit": "L"}
                    ],
                    "cost": 18.75,
                    "category": "Main Course"
                }
            ]
            with open(recipes_file, 'w') as f:
                json.dump(sample_recipes, f, indent=4)
        
        # Sample orders
        orders_file = os.path.join(self.data_dir, "orders.json")
        if not os.path.exists(orders_file):
            sample_orders = [
                {
                    "id": 1,
                    "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                    "items": [
                        {"recipe_id": 1, "quantity": 5},
                        {"recipe_id": 2, "quantity": 3}
                    ],
                    "total": 118.75,
                    "status": "Completed"
                },
                {
                    "id": 2,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "items": [
                        {"recipe_id": 1, "quantity": 2}
                    ],
                    "total": 25.00,
                    "status": "In Progress"
                }
            ]
            with open(orders_file, 'w') as f:
                json.dump(sample_orders, f, indent=4)
    
    def get_inventory(self):
        """Get all inventory items"""
        try:
            with open(os.path.join(self.data_dir, "inventory.json"), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading inventory: {e}")
            return []
    
    def get_recipes(self):
        """Get all recipes"""
        try:
            with open(os.path.join(self.data_dir, "recipes.json"), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading recipes: {e}")
            return []
    
    def get_orders(self):
        """Get all orders"""
        try:
            with open(os.path.join(self.data_dir, "orders.json"), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading orders: {e}")
            return []
    
    def update_inventory_item(self, item_id, updates):
        """Update an inventory item"""
        try:
            inventory = self.get_inventory()
            for i, item in enumerate(inventory):
                if item["id"] == item_id:
                    inventory[i].update(updates)
                    break
                    
            with open(os.path.join(self.data_dir, "inventory.json"), 'w') as f:
                json.dump(inventory, f, indent=4)
            return True
        except Exception as e:
            print(f"Error updating inventory item: {e}")
            return False
    
    def add_inventory_item(self, item):
        """Add a new inventory item"""
        try:
            inventory = self.get_inventory()
            # Generate new ID
            new_id = max([i["id"] for i in inventory], default=0) + 1
            item["id"] = new_id
            inventory.append(item)
            
            with open(os.path.join(self.data_dir, "inventory.json"), 'w') as f:
                json.dump(inventory, f, indent=4)
            return True
        except Exception as e:
            print(f"Error adding inventory item: {e}")
            return False
    
    def delete_inventory_item(self, item_id):
        """Delete an inventory item"""
        try:
            inventory = self.get_inventory()
            inventory = [item for item in inventory if item["id"] != item_id]
            
            with open(os.path.join(self.data_dir, "inventory.json"), 'w') as f:
                json.dump(inventory, f, indent=4)
            return True
        except Exception as e:
            print(f"Error deleting inventory item: {e}")
            return False
    
    def update_recipe(self, recipe_id, updates):
        """Update a recipe"""
        try:
            recipes = self.get_recipes()
            for i, recipe in enumerate(recipes):
                if recipe["id"] == recipe_id:
                    recipes[i].update(updates)
                    break
                    
            with open(os.path.join(self.data_dir, "recipes.json"), 'w') as f:
                json.dump(recipes, f, indent=4)
            return True
        except Exception as e:
            print(f"Error updating recipe: {e}")
            return False
    
    def add_recipe(self, recipe):
        """Add a new recipe"""
        try:
            recipes = self.get_recipes()
            # Generate new ID
            new_id = max([r["id"] for r in recipes], default=0) + 1
            recipe["id"] = new_id
            recipes.append(recipe)
            
            with open(os.path.join(self.data_dir, "recipes.json"), 'w') as f:
                json.dump(recipes, f, indent=4)
            return True
        except Exception as e:
            print(f"Error adding recipe: {e}")
            return False
    
    def add_order(self, order):
        """Add a new order"""
        try:
            orders = self.get_orders()
            # Generate new ID
            new_id = max([o["id"] for o in orders], default=0) + 1
            order["id"] = new_id
            orders.append(order)
            
            with open(os.path.join(self.data_dir, "orders.json"), 'w') as f:
                json.dump(orders, f, indent=4)
            return True
        except Exception as e:
            print(f"Error adding order: {e}")
            return False
    
    def update_order_status(self, order_id, status):
        """Update an order's status"""
        try:
            orders = self.get_orders()
            for i, order in enumerate(orders):
                if order["id"] == order_id:
                    orders[i]["status"] = status
                    break
                    
            with open(os.path.join(self.data_dir, "orders.json"), 'w') as f:
                json.dump(orders, f, indent=4)
            return True
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False