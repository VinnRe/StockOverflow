class Recipe:
    def __init__(self, recipe_id, recipe_name, ingredients):
        """
        Represents a Recipe.
        :param recipe_id: Unique ID for the recipe (Firebase key)
        :param recipe_name: Name of the recipe
        :param ingredients: Dictionary of ingredient names and required quantities
        """
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.ingredients = ingredients

    def to_dict(self):
        """
        Convert the Recipe object into a dictionary format for Firebase storage.
        """
        return {
            "recipeName": self.recipe_name,
            "ingredients": self.ingredients
        }