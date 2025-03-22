from controllers.staff_controller import StaffController
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

def interactive_recipe_test():
    """Interactive menu to test RecipeController functions."""
    recipe_ctrl = StaffController()

    while True:
        print("\n========== Recipe Management ==========")
        print("1. Display All Recipes")
        print("2. Add a New Recipe")
        print("3. Order a Recipe")
        print("4. Delete a Recipe")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n--- Displaying Recipes ---")
            recipe_ctrl.viewAllRecipes()

        elif choice == "2":
            print("\n--- Adding a New Recipe ---")
            recipe_name = input("Enter recipe name: ")
            ingredient_dict = {}

            while True:
                ingredient = input("Enter ingredient name (or type 'done' to finish): ")
                if ingredient.lower() == "done":
                    break
                quantity = input(f"Enter quantity for {ingredient}: ")
                if quantity.isdigit():
                    ingredient_dict[ingredient] = int(quantity)
                else:
                    print("Invalid quantity. Please enter a number.")

            recipe_ctrl.addRecipe(recipe_name, ingredient_dict)

        elif choice == "3":
            print("\n--- Ordering a Recipe ---")
            recipe_id = input("Enter Recipe ID to order: ")
            recipe_ctrl.orderRecipe(recipe_id)

        elif choice == "4":
            print("\n--- Deleting a Recipe ---")
            recipe_id = input("Enter Recipe ID to delete: ")
            confirm = input(f"Are you sure you want to delete recipe '{recipe_id}'? (y/n): ")
            if confirm.lower() == 'y':
                recipe_ctrl.deleteRecipe(recipe_id)

        elif choice == "5":
            print("\nExiting Recipe Management. Goodbye!")
            break

        else:
            print("\nInvalid choice! Please enter a number between 1-5.")

if __name__ == "__main__":
    interactive_recipe_test()
