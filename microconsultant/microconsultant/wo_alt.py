import frappe

def alt_items(self, method):
	stock_dict={}
	rq_items = self.get("required_items")
	for d in self.get('required_items'):
		if d.alternate == 0:
			if d.available_qty_at_source_warehouse<d.required_qty:
				rq = d.required_qty - d.available_qty_at_source_warehouse
				altic = frappe.db.get_list('Item Alternative',filters={'item_code':d.item_code,'product_specific_alternatives':0},fields=['alternative_item_code'],pluck='alternative_item_code')
				for a in altic:
					if frappe.db.exists('Bin',{'item_code':a,'warehouse':d.source_warehouse}):
						alt_stock = frappe.db.get_value('Bin',{'item_code':a,'warehouse':d.source_warehouse},'projected_qty')
						if alt_stock > 0:
							stock_dict.update({a:alt_stock})
				sorted_stock ={k: v for k,v in sorted(stock_dict.items(), key= lambda v: v[1])}
				for x,y in sorted_stock.items():
					if x in altic:
						if d.required_qty <=0:
							self.remove(d)
							break
						else:	
							rqp = rq - y
							if rqp<= 0:
								item = frappe.get_doc(self)
								items = item.append('required_items',{})
								items.item_code = x
								items.required_qty = rq
								d.required_qty = d.required_qty - items.required_qty
								items.idx = d.idx
								items.source_warehouse = d.source_warehouse 
								items.alternate = 1
								items.alternate_of = d.item_code
							# items.insert()
								inventory = y-rq
								stock_dict.update({x:inventory})
								items.insert()
							elif y>0:
								item = frappe.get_doc(self)
								items = item.append('required_items',{})
								items.item_code = x
								items.alternate = 1
								items.required_qty = y
								d.required_qty = d.required_qty - items.required_qty
								items.alternate_of = d.item_code
								items.source_warehouse = d.source_warehouse
								items.idx = d.idx
								# items.insert()
								stock_dict.update({x:0})
								items.insert()

def ps_alt(self):
	stock_dict={}
	for d in self.get('required_items'):
		product_specific = frappe.db.sql_list("""SELECT alternatives FROM `tabAlt Items` WHERE parent=%s""",self.production_item)
		if d.available_qty_at_source_warehouse<d.required_qty:
			rq = d.required_qty - d.available_qty_at_source_warehouse
			altic = frappe.db.get_list('Item Alternative',filters={'item_code':d.item_code,'product_specific_alternatives':1},fields=['alternative_item_code'],pluck='alternative_item_code')
			for a in altic:
				if a in product_specific:
					alt_stock = frappe.db.get_value('Bin',{'item_code':a,'warehouse':d.source_warehouse},'projected_qty')
					if alt_stock >0:
						stock_dict.update({a:alt_stock})
						sorted_stock ={k: v for k,v in sorted(stock_dict.items(), key= lambda v: v[1])}
					for x,y in sorted_stock.items():
						if x in altic:
							if d.required_qty <=0:
								self.remove(d)
								break
							else:
								rqp = rq - y
								if rqp<= 0:
									item = frappe.get_doc(self)
									items = item.append('required_items',{})
									items.item_code = x
									items.required_qty = rq
									items.idx = d.idx
									d.required_qty = d.required_qty - items.required_qty
									items.alternate = 1
									items.source_warehouse = d.source_warehouse
									items.alternate_of = d.item_code
									# items.insert()
									inventory = y-rq
									stock_dict.update({x:inventory})
									items.insert()
								elif y>0:
									item = frappe.get_doc(self)
									items = item.append('required_items',{})
									items.item_code = x
									items.alternate = 1
									items.required_qty = y
									items.source_warehouse = d.source_warehouse
									d.required_qty = d.required_qty - items.required_qty
									items.alternate_of = d.item_code				
									items.idx = d.idx
									# items.insert()
									stock_dict.update({x:0})
									items.insert()

def stock_entry(self,method):
	wo = frappe.get_doc("Work Order",self.work_order)
	item_list = []
	for d in self.get('items'):
		item_list.append(d.item_code)
	for i in wo.get('required_items'):
		if i.item_code not in item_list and i.required_qty >0:
			item = frappe.get_doc(self)
			items = item.append('items',{})
			items.item_code = i.item_code
			items.custom_alternate = 1
			items.qty = i.required_qty
			items.s_warehouse = i.source_warehouse
			items.custom_alternate_of = d.item_code				
			# items.insert()
			items.uom = frappe.db.get_value("Item",i.item_code,"stock_uom")
			items.stock_uom = frappe.db.get_value("Item",i.item_code,"stock_uom")
			items.conversion_factor = frappe.db.get_value("UOM Conversion Detail",{"parent":i.item_code,"uom":frappe.db.get_value("Item",i.item_code,"stock_uom"),"conversion_factor")
			item.set_missing_values()
			items.insert()
