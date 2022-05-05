import frappe

def alt_items(self, method):
	wo_ps(self)
	stock_dic={}
	stock = 0.0
	alt_stock = 0.0
	item = self.get("required_items")
	for d in item[:]:
		stocks = frappe.db.sql_list("""SELECT actual_qty FROM `tabBin` WHERE item_code=%s""",d.item_code)
		for k in stocks:
			stock = stock + k
		stock_dic.update({d.item_code:stock})
		manufacturers = frappe.db.sql_list("""SELECT manufacturer_part_no FROM `tabItem Manufacturer` WHERE item_code = %s""",d.item_code)
		altic = frappe.db.sql_list("""SELECT alternative_item_code FROM `tabItem Alternative` WHERE item_code = %s AND product_specific_alternatives=0""",d.item_code)
		for a in altic:
			alt_stocks = frappe.db.sql_list("SELECT actual_qty FROM `tabBin` WHERE item_code=%s",a)
			for o in alt_stocks:
				alt_stock = alt_stock + o
			if a in stock_dic:
				print("%s stock",a)
				break
			stock_dic.update({a:alt_stock})	
		for i in range(0, len(altic)):
			item_supplier = frappe.db.get_value('Item Supplier',{"parent":'Item', "parent":altic[i]},'supplier')
			print(stock_dic[altic[i]])
			if stock_dic[altic[i]] != 0:
				doc = frappe.get_doc(self)
				row = doc.append('required_items',{})
				row.item_code = altic[i]
				row.required_qty = d.required_qty
				row.description = altic[i]
				row.source_warehouse = d.source_warehouse
				row.insert()

def wo_ps(self):
	stock_dic={}
	product_specific = frappe.db.sql_list("""SELECT alternatives FROM `tabAlt Items` WHERE parent=%s""",self.production_item)
	for p in product_specific:
		itm = frappe.db.sql_list("""SELECT item_code FROM `tabItem Alternative` WHERE alternative_item_code = %s AND product_specific_alternatives=1""",p)
		if itm != []:
			it = self.get("required_items")
			for d in it[:]:
				for z in itm:
					alt_stock=0.0
					alt_stocks = frappe.db.sql_list("""SELECT actual_qty FROM `tabBin` WHERE item_code=%s""",p)
					for k in alt_stocks:
						alt_stock = alt_stock +k
					if d in stock_dic:
						break
					stock_dic.update({p:alt_stock})
					if stock_dic[p] == None :
						stock_dic.update({p:0})
					if stock_dic[p] != 0:
						if d.item_code == z:
							doc = frappe.get_doc(self)
							row = doc.append('required_items',{})
							row.item_code = p
							row.required_qty = d.required_qty
							row.description = altic[i]
							row.source_warehouse = d.source_warehouse
							row.insert()	