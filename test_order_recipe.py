from controllers.staff_controller import StaffController

# Initialize StaffController
staff_controller = StaffController()

# Fetch all recipes before ordering
print("\n>>> Fetching Recipes...")
staff_controller.get_recipes()

# Ask user to enter a recipe name to order
recipe_name = input("\nEnter the recipe you want to order: ")

# Order the recipe
print("\n>>> Ordering Recipe...")
staff_controller.order_recipe(recipe_name)