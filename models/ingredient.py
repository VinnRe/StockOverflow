class Ingredient:
    def __init__(self):
        # Dictionary to store ingredients and their quantities
        self.ingredients = {}

    def add_ingredient(self, ingredient, quantity):
        # Add or update an ingredient with the specified quantity
        self.ingredients[ingredient] = int(quantity)
        return self.ingredients