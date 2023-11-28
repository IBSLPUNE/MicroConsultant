import frappe

def alt_items(self, method):
	stock_dict={}
	rq_items = self.get('required_items')
	for d in rq_items[:]:
		if d.alternate ==0:
			if d.available_qty_at_source_warehouse<d.required_qty:
				rq = d.required_qty - d.available_qty_at_source_warehouse
				altic = frappe.db.get_list('Item Alternative',filters={'item_code':d.item_code,'product_specific_alternatives':0},fields=['alternative_item_code'],pluck='alternative_item_code')
				for a in altic:
					alt_stock = frappe.db.get_value('Bin',{'item_code':a,'warehouse':d.source_warehouse},'projected_qty')
					if alt_stock >0:
						stock_dict.update({a:alt_stock})
				sorted_stock ={k: v for k,v in sorted(stock_dict.items(), key= lambda v: v[1])}
				frappe.errprint("sortted_stock":sorted_stock)
				for x,y in sorted_stock.items():
					rqp = rq - y
					if rqp<= 0:
						item = frappe.get_doc(self)
						items = item.append('required_items',{})
						items.item_code = x
						items.required_qty = rq
						d.required_qty = d.required_qty - items.required_qty
						items.idx = d.idx + 1
						items.source_warehouse = d.source_warehouse 
						items.alternate = 1
						for i in rq_items[:]:
							if i.idx >= d.idx +1:
								i.idx=i.idx +1
						items.alternate_of = d.item_code
						items.insert()
						inventory = y-rq
						stock_dict.update({x:inventory})
					elif y>0:
						item = frappe.get_doc(self)
						items = item.append('required_items',{})
						items.item_code = x
						items.alternate = 1
						items.required_qty = y
						d.required_qty = d.required_qty - items.required_qty
						for i in rq_items[:]:
							if i.idx >= d.idx +1:
								i.idx=i.idx +1
						items.alternate_of = d.item_code
						items.idx = d.idx + 1
						items.insert()
						stock_dict.update({x:0})

def ps_alt(self):
	stock_dict={}
	rq_items = self.get('required_items')
	for d in rq_items[:]:
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
						rqp = rq - y
						if rqp<= 0:
							item = frappe.get_doc(self)
							items = item.append('required_items',{})
							items.item_code = x
							items.required_qty = rq
							items.idx = d.idx + 1
							d.required_qty = d.required_qty - items.required_qty
							items.alternate = 1
							for i in rq_items[:]:
								if i.idx >= d.idx +1:
									i.idx = i.idx +1
							items.alternate_of = d.item_code
							items.insert()
							inventory = y-rq
							stock_dict.update({x:inventory})
						elif y>0:
							item = frappe.get_doc(self)
							items = item.append('required_items',{})
							items.item_code = x
							items.alternate = 1
							items.required_qty = y
							d.required_qty = d.required_qty - items.required_qty
							for i in rq_items[:]:
								if i.idx >= d.idx +1:
									i.idx=i.idx +1
							items.alternate_of = d.item_code				
							items.idx = d.idx + 1
							items.insert()
							stock_dict.update({x:0})
							stock_dict.update({x:0})
