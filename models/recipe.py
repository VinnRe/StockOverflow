class Recipe:
    def __init__(self, recipe_name, ingredients):
        # Initialize recipe name and ingredients with required quantities
        self.recipe_name = recipe_name
        self.ingredients = ingredients

    def to_dict(self):
        # Convert object properties to a dictionary for storage
        return {
            "recipeName": self.recipe_name,
            "ingredients": self.ingredients
        }
