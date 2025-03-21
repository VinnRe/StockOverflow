"""
Helper functions and utilities for StockOverflow
"""

import os
import json
from datetime import datetime, timedelta

def format_currency(amount):
    """Format a number as currency"""
    return f"${amount:.2f}"

def calculate_days_until(date_str):
    """Calculate days until a given date"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        delta = date - datetime.now()
        return delta.days
    except:
        return 0

def is_expiring_soon(date_str, days=7):
    """Check if a date is expiring soon"""
    days_left = calculate_days_until(date_str)
    return 0 <= days_left <= days

def is_expired(date_str):
    """Check if a date is expired"""
    days_left = calculate_days_until(date_str)
    return days_left < 0

def is_low_stock(quantity, threshold=10):
    """Check if an item is low in stock"""
    return quantity < threshold

def get_item_by_id(items, item_id):
    """Get an item by ID from a list"""
    for item in items:
        if item["id"] == item_id:
            return item
    return None

def calculate_recipe_cost(recipe, inventory):
    """Calculate the cost of a recipe based on ingredients"""
    total_cost = 0
    for ingredient in recipe["ingredients"]:
        item = get_item_by_id(inventory, ingredient["item_id"])
        if item:
            # This is a simplified calculation
            # In a real system, you'd have cost per unit for each inventory item
            total_cost += ingredient["quantity"] * 2.5  # Placeholder cost
    return total_cost

def generate_analytics_data(inventory, recipes, orders):
    """Generate analytics data from inventory, recipes, and orders"""
    # Calculate total inventory value
    inventory_value = sum(item["quantity"] * 2.5 for item in inventory)  # Placeholder cost
    
    # Calculate expiring soon items
    expiring_soon = [item for item in inventory if is_expiring_soon(item["expiry"])]
    
    # Calculate low stock items
    low_stock = [item for item in inventory if is_low_stock(item["quantity"])]
    
    # Calculate sales by category
    sales_by_category = {}
    for order in orders:
        for item in order["items"]:
            recipe = get_item_by_id(recipes, item["recipe_id"])
            if recipe:
                category = recipe["category"]
                if category not in sales_by_category:
                    sales_by_category[category] = 0
                sales_by_category[category] += item["quantity"]
    
    return {
        "inventory_value": inventory_value,
        "expiring_soon_count": len(expiring_soon),
        "low_stock_count": len(low_stock),
        "sales_by_category": sales_by_category
    }