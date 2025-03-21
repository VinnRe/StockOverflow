import firebase_admin
from firebase_admin import credentials

from models.inventory import InventoryItem
from controllers.foodInventory import FoodInventory

cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://inventrial-f2112-default-rtdb.firebaseio.com/'
})


item = InventoryItem("x", "bb1z", "cc1z", "dd1z", "ee1z")
foodInventory = FoodInventory()

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
# foodInventory.removeItem("-OLu0sSsrtMriiTPGfJJ")