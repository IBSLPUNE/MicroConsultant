import frappe

def filter_items(self, method):
	items = self.get('items')
	for item in items[:]:
		if not frappe.db.exists("Item Supplier",{"supplier":self.supplier, "parent":item.item_code}):
			self.remove(item)
