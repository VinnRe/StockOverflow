from firebase_admin import db

class FoodInventory:
	def __init__(self):
		self.ref = db.reference('db')
		self.items_ref = self.ref.child('inventory')

	def displayItems(self):
		items = []
		itemsObj = self.items_ref.get()
		for key, value in itemsObj.items():
			items.append({key: value})

		return items

	def searchItemById(self, itemId):
		itemQry = self.items_ref.order_by_key().equal_to(itemId).limit_to_first(1).get()
		if itemQry:
			# print({itemId: itemQry[itemId]})
			return {itemId: itemQry[itemId]}
	
	def searchItemByName(self, itemName):
		itemQry = self.items_ref.order_by_child("itemName").equal_to(itemName).limit_to_first(1).get()
		if itemQry:
			# print({itemName: itemQry[list(itemQry)[0]]})
			return {itemName: itemQry[list(itemQry)[0]]}

	def changeQuantity(self, itemId, quantity):
		self.items_ref.child(itemId).update({"quantity": quantity})



	# admin only
	def createItem(self, item):
		item = {
			"itemName": item.itemName,
			"itemCategory": item.itemCategory,
			"quantity": item.quantity,
			"unit": item.unit,
			"expiryDate": item.expiryDate
		}
		self.items_ref.push(item)

		return item

	def updateItem(self, itemId, item):
		self.items_ref.child(itemId).update(item)

	def removeItem(self, itemId):
		self.items_ref.child(itemId).delete()