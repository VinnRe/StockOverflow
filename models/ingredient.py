class Ingredient:
	def __init__(self):
		self.ingredients = []

	def addIngredient(self, ingredient, quantity):
		self.ingredients.append({
			"ingredient": ingredient, 
			"quantity": quantity
		})
		return self.ingredients

	def getIngredients(self):
		# print(self.ingredients)
		return self.ingredients

	def removeIngredient(self, ingredient):
		self.ingredients = [item for item in self.ingredients if item["ingredient"] != ingredient]
		return self.ingredients

	def editIngredient(self, ingredient, quantity):
		for item in self.ingredients:
			if item["ingredient"] == ingredient:
				item["quantity"] = quantity
				break

		# print(self.ingredients)
		return self.ingredients

