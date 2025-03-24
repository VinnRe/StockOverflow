class Ingredient:
	def __init__(self):
		self.ingredients = {}

	def add_ingredient(self, ingredient, quantity):
		self.ingredients[ingredient] = int(quantity)
		return self.ingredients