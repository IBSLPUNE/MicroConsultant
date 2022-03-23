import frappe
from frappe.utils import (
	add_days,
	ceil,
	cint,
	comma_and,
	flt,
	get_link_to_form,
	getdate,
	now_datetime,
	nowdate,
)
from frappe import _, msgprint




def add_items(self, method):
	stock_dic={}
	items = self.get("mr_items")
	psalt(self)
	for d in items[:]:
		qty_oh=0.0
		qty_or=0.0
		stock = frappe.db.get_value("Bin",{'item_code':d.item_code,'warehouse':d.warehouse},"actual_qty")
		stock_dic.update({d.item_code:stock})
		altic = frappe.db.sql_list("""SELECT alternative_item_code FROM `tabItem Alternative` WHERE item_code = %s AND product_specific_alternatives=0""",d.item_code)
		for a in altic:
			alt_stocks = frappe.db.get_value("Bin",{'item_code':a,'warehouse':d.warehouse},"actual_qty")
			if a in stock_dic:
				print("%s stock",a)
				break
			stock_dic.update({a:alt_stocks})
			if stock_dic[a] == None :
				stock_dic.update({a:0})
			qty_oh = qty_oh + stock_dic[a]
		qty_oh += d.actual_qty
		qty_or = d.required_bom_qty - qty_oh
		if qty_or <= 0:
			self.remove(d)
			message = _("As there are sufficient raw materials alternate included, Material Request is not required for Warehouse {0}.").format(d.warehouse) + "<br><br>"
			frappe.msgprint(message, title=_("Note"))
		else:
			d.quantity = qty_or
			#d.save()
		for a in altic:
			if qty_or >= 0:
				stock_dic.update({a:0})
			else:
				req_qty = d.required_bom_qty - d.actual_qty
				sorted_stock ={k: v for k,v in sorted(stock_dic.items(), key= lambda v: v[1])}
				for x,y in sorted_stock.items():
					req_qty -= y
					if req_qty < 0:
						break
				req_qty = abs(req_qty)
				stock_dic.update({x:req_qty})

def psalt(self):
	stock_dic={}
	for k in self.get("po_items"):
		product_specific = frappe.db.sql_list("""SELECT alternatives FROM `tabAlt Items` WHERE parent=%s""",k.item_code)
		for p in product_specific:
			item = frappe.db.sql_list("""SELECT item_code FROM `tabItem Alternative` WHERE alternative_item_code = %s AND product_specific_alternatives=1""",p)
			if item != []:
				it = self.get("mr_items")
				for d in it[:]:
					if d.item_code == item[0]:
						qty_oh=0.0
						qty_or=0.0
						stock = frappe.db.get_value("Bin",{'item_code':item[0],'warehouse':d.warehouse},"actual_qty")
						stock_dic.update({item[0]:stock})
						alt_stocks = frappe.db.get_value("Bin",{'item_code':p,'warehouse':d.warehouse},"actual_qty")
						if d in stock_dic:
							break
						stock_dic.update({p:alt_stocks})
						if stock_dic[p] == None :
							stock_dic.update({p:0})
							qty_oh = qty_oh + stock_dic[p]
						qty_oh += d.actual_qty
						qty_or = d.required_bom_qty - qty_oh
						if qty_or <= 0:
							self.remove(d)
							message = _("As there are sufficient raw materials alternate{0} included, Material Request is not required for Warehouse {0}.").format(item[0],d.warehouse) + "<br><br>"
							frappe.msgprint(message, title=_("Note"))
						else:
							d.quantity = qty_or
						if qty_or >= 0:
							stock_dic.update({p:0})
						else:
							req_qty = d.required_bom_qty - d.actual_qty
							sorted_stock ={k: v for k,v in sorted(stock_dic.items(), key= lambda v: v[1])}
							for x,y in sorted_stock.items():
								req_qty -= y
								if req_qty < 0:
									break
							req_qty = abs(req_qty)
							stock_dic.update({x:req_qty})








						


			


		
def rfq_items(self, method):
	rfq_ps(self)
	i = self.get('items')
	for d in i[:]:
		manufacturers = frappe.db.sql_list("""SELECT manufacturer_part_no FROM `tabItem Manufacturer` WHERE item_code = %s""",d.item_code)
		for a in manufacturers:
			if d.manufacturer_part_no != a:
				item = frappe.get_doc(self)
				items = item.append('items',{})
				items.item_code = d.item_code
				items.qty = d.qty
				items.manufacturer_part_no = a
				items.warehouse = d.warehouse
				item.schedule_date = d.schedule_date
				item.set_missing_values()
				items.insert()
		altic = {}
		altic = frappe.db.sql_list("""SELECT alternative_item_code FROM `tabItem Alternative` WHERE item_code = %s AND product_specific_alternatives=0""",d.item_code)
		manufacturers = frappe.db.sql_list("""SELECT manufacturer_part_no FROM `tabItem Manufacturer` WHERE item_code = %s""",d.item_code)

		
		for i in range(0, len(altic)):
			item_supplier = frappe.db.get_value('Item Supplier',{"parent":'Item', "parent":altic[i]},'supplier')
			item_manufacturers = frappe.db.sql_list("""SELECT manufacturer_part_no FROM `tabItem Manufacturer` WHERE item_code = %s""",altic[i])
			if item_manufacturers == []:
				frappe.throw("Add item_manufacturers for item "+ altic[i])
			for s in self.get('suppliers'):
				for m in range(0, len(item_manufacturers)):
					if s.supplier == item_supplier:
						doc = frappe.get_doc(self)
						row = doc.append('items',{})
						row.item_code = altic[i]
						row.qty = d.qty
						row.description = altic[i]
						row.uom = "Nos"
						row.conversion_factor = 1
						row.warehouse = d.warehouse
						row.schedule_date = d.schedule_date
						row.manufacturer_part_no = item_manufacturers[m]
						row.insert()

def rfq_ps(self):
	for a in self.get("items"):
		mr = frappe.db.get_value("Material Request Item",{'parent':a.material_request},"production_plan")
		break
	p = frappe.get_doc("Production Plan", mr)
	for i in p.get("po_items"):
		item = frappe.get_doc(self)
		items = item.append('products', {})
		items.item_code = i.item_code
		items.bom_no = i.bom_no
		items.planned_qty = i.planned_qty
		items.planned_start_date = i.planned_start_date
		items.insert()
	products = self.get("products")
	for a in products[:]:
		product_specific = frappe.db.sql_list("""SELECT alternatives FROM `tabAlt Items` WHERE parent=%s""",a.item_code)
		for p in product_specific:
			item = frappe.db.sql_list("""SELECT item_code FROM `tabItem Alternative` WHERE alternative_item_code = %s AND product_specific_alternatives=1""",p)
			if item != []:
				it = self.get("items")
				for d in it[:]:
					if d.item_code == item[0]:
						item_supplier = frappe.db.get_value('Item Supplier',{"parent":'Item', "parent":p},'supplier')
						item_manufacturers = frappe.db.sql_list("""SELECT manufacturer_part_no FROM `tabItem Manufacturer` WHERE item_code = %s""",p)
						if item_manufacturers == []:
							frappe.throw("Add item_manufacturers for item "+ p)
						for s in self.get('suppliers'):
							for m in range(0, len(item_manufacturers)):
								if s.supplier == item_supplier:
									doc = frappe.get_doc(self)
									row = doc.append('items',{})
									row.item_code = p
									row.qty = d.qty
									row.warehouse = d.warehouse
									row.schedule_date = d.schedule_date
									row.manufacturer_part_no = item_manufacturers[m]
									doc.set_missing_values()
									row.insert()







