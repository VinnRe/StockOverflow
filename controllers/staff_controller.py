from firebase_admin import db

class StaffController:
    def __init__(self):
        self.ref = db.reference('db')
        self.recipes_ref = self.ref.child('recipes')
        self.inventory_ref = self.ref.child('inventory')
    
    def addRecipe(self, recipe):
        """Add a new recipe to the database."""
        try:
            new_ref = self.recipes_ref.push(recipe)
            print(f"Added new recipe: {recipe['recipeName']}")
            return {new_ref.key: recipe}
        except Exception as e:
            print(f"Error adding recipe: {e}")
            return None
    
    def viewAllRecipes(self):
        """Retrieve and display all recipes."""
        try:
            recipes = self.recipes_ref.get()
            if not recipes:
                print("No recipes found.")
                return []
            
            recipe_list = []
            print("\n Available Recipes:")
            for recipe_id, recipe_data in recipes.items():
                print(f"\n {recipe_id} | {recipe_data['recipeName']}")
                for ingredient, quantity in recipe_data.get("ingredients", {}).items():
                    print(f"   - {quantity}x {ingredient}")
                
                recipe_list.append({recipe_id: recipe_data})
            
            return recipe_list
        except Exception as e:
            print(f"Error retrieving recipes: {e}")
            return []

    def orderRecipe(self, recipeId):
        """Order a recipe by checking inventory and updating stock."""
        try:
            recipe = self.recipes_ref.child(recipeId).get()
            if not recipe:
                print(f"No recipe found with ID: {recipeId}")
                return False
            
            ingredients = recipe.get("ingredients", {})
            for itemName, requiredQty in ingredients.items():
                items = self.inventory_ref.order_by_child("itemName").equal_to(itemName).get()
                if not items:
                    print(f"Insufficient stock for {itemName}")
                    return False
                
                for item_id, item_data in items.items():
                    stock = item_data.get("stock", {})
                    totalQuantity = item_data.get("totalQuantity", 0)
                    if totalQuantity < requiredQty:
                        print(f"Not enough {itemName} in stock.")
                        return False
                    
                    # Deduct stock based on expiry date order
                    sorted_stock = sorted(stock.items(), key=lambda x: x[0])
                    deducted = 0
                    for expiryDate, quantity in sorted_stock:
                        if deducted >= requiredQty:
                            break
                        toDeduct = min(requiredQty - deducted, quantity)
                        stock[expiryDate] -= toDeduct
                        deducted += toDeduct
                        if stock[expiryDate] == 0:
                            del stock[expiryDate]
                    
                    # Update Firebase
                    totalQuantity -= requiredQty
                    self.inventory_ref.child(item_id).update({
                        "stock": stock,
                        "totalQuantity": totalQuantity
                    })
            
            print(f"Successfully ordered recipe: {recipe['recipeName']}")
            return True
        except Exception as e:
            print(f"Error ordering recipe: {e}")
            return False