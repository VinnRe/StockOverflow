import firebase_admin
from firebase_admin import credentials

from models.ingredient import Ingredient
from models.inventory import InventoryItem
from controllers.recipe import Recipe
from controllers.foodInventory import FoodInventory

cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://stockoverflow-b4e38-default-rtdb.firebaseio.com/'
})



ingredient = Ingredient()
ingredient.addIngredient("asin", 5)
ingredient.addIngredient("chimken", 15)
ingredient.getIngredients()
ingredient.removeIngredient("asin")
ingredient.getIngredients()
ingredient.editIngredient("chimken", 33)

recipe = Recipe()
recipe.addRecipe("Abobo", ingredient)

# item = InventoryItem("x", "bb1z", "cc1z", "dd1z", "ee1z")
# foodInventory = FoodInventory()
# foodInventory.createItem(item)
# foodInventory.displayItems()
# foodInventory.searchItemById("-OLu0LbMNws4WhoTDN_v")
# foodInventory.searchItemByName("toyosukaburger")
# foodInventory.changeQuantity("-OLtif-of2snMjeSpeyP", 115)
# foodInventory.updateItem("-OLtif-of2snMjeSpeyP", {
#     "expiryDate": "xx",
#     "itemCategory": "qwe",
#     "itemName": "toyosukaburger",
#     "quantity": 35,
#     "unit": "unitt"
#     })
# foodInventory.deleteItem("-OLu0sSsrtMriiTPGfJJ")