from firebase_admin import db

class Recipe:
	def __init__(self):
		self.ref = db.reference('db')
		self.recipes_ref = self.ref.child('recipes')

	def addRecipe(self, recipeName, ingredientObj):
		recipe = {
			"recipeName": recipeName,
			"ingredients": ingredientObj.getIngredients()
		}
		self.recipes_ref.push(recipe)
		return recipe

	def updateRecipe(self, recipeId, recipeName, ingredientObj):
		self.recipes_ref.child(recipeId).update({
			"recipeName": recipeName, 
			"ingredients": ingredientObj.getIngredients()
		})

	def deleteRecipe(self, recipeId):
		self.recipes_ref.child(recipeId).delete()

	def getAllRecipes(self):
		return self.recipes_ref.get()

	# def displayRecipe(self):


