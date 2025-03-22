import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
from controllers.food_inventory_controller import FoodInventory  # Import your class

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Initialize Firebase Admin SDK (Make sure your .env has DB_URL set)
cred = credentials.Certificate("key.json")  # Update path
firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})

# Initialize Inventory System
inventory = FoodInventory()

def main():
    while True:
        print("\n===== Food Inventory Management =====")
        print("1. Display All Items")
        print("2. Search Item by ID")
        print("3. Search Item by Name")
        print("4. Change Item Quantity")
        print("5. Add New Item")
        print("6. Update Item")
        print("7. Delete Item")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            items = inventory.displayItems()
            print("\nInventory Items:")
            for item in items:
                print(item)

            # print("\nNear Expiry Date:")
            # for item in result['items_near_expiry_date']:
            #     print(item)

            # print("\nLow Stocks:")
            # for item in result['item_low_stock']:
            #     print(item)

        elif choice == "2":
            item_id = input("\nEnter Item ID: ")
            result = inventory.searchItemById(item_id)
            print("\nSearch Result:", result if result else "Item not found.")

        elif choice == "3":
            item_name = input("\nEnter Item Name: ")
            result = inventory.searchItemByName(item_name)
            print("\nSearch Result:", result if result else "Item not found.")

        elif choice == "4":
            item_id = input("\nEnter Item ID: ")
            expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
            quantity = int(input("Enter New Quantity: "))
            inventory.changeQuantity(item_id, expiry_date, quantity)
            print("\nQuantity Updated.")

        elif choice == "5":
            print("\nAdd New Item")
            item_name = input("Item Name: ")

            # Collect stock information
            stock = {}
            while True:
                expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
                quantity = int(input("Enter Quantity for this expiry date: "))
                stock[expiry_date] = quantity

                more = input("Add another expiry date for this item? (yes/no): ").strip().lower()
                if more != "yes":
                    break

            item = {
                "itemName": item_name,
                "stock": stock
            }
            inventory.createItem(item)
            print("\nItem Added.")

        elif choice == "6":
            item_id = input("\nEnter Item ID: ")
            print("\nUpdate Item (Leave blank to skip a field)")
            updated_data = {}

            name = input("New Item Name: ")
            if name:
                updated_data["itemName"] = name

            update_stock = input("Do you want to update stock? (yes/no): ").strip().lower()
            if update_stock == "yes":
                stock = {}
                while True:
                    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
                    quantity = int(input("Enter Quantity for this expiry date: "))
                    stock[expiry_date] = quantity

                    more = input("Add another expiry date for this item? (yes/no): ").strip().lower()
                    if more != "yes":
                        break

                updated_data["stock"] = stock

            inventory.updateItem(item_id, updated_data)
            print("\nItem Updated.")

        elif choice == "7":
            item_id = input("\nEnter Item ID to Delete: ")
            inventory.deleteItem(item_id)
            print("\nItem Deleted.")

        elif choice == "8":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()