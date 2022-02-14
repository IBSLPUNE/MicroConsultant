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
	for d in self.get("mr_items"):
		qty_oh=0.0
		qty_or=0.0
		stock = frappe.db.get_value("Bin",{'item_code':d.item_code,'warehouse':d.warehouse},"actual_qty")
		stock_dic.update({d.item_code:stock})
		altic = frappe.db.sql_list("""SELECT alternative_item_code FROM `tabItem Alternative` WHERE item_code = %s""",d.item_code)
		if altic == None:
			break
		for a in altic:
			alt_stocks = frappe.db.get_value("Bin",{'item_code':a,'warehouse':d.warehouse},"actual_qty")
			if a in stock_dic:
				break
			stock_dic.update({a:alt_stocks})
			if stock_dic[a] == None :
				stock_dic.update({a:0})
			qty_oh = qty_oh + stock_dic[a]
		print(stock_dic)
		qty_oh += d.actual_qty
		qty_or = d.required_bom_qty - qty_oh
		print(qty_or)
		if qty_or >= 0:
			d.quantity = qty_or
		else:
			d.remove()
			message = _("As there are sufficient raw materials, Material Request is not required for Warehouse {0}.").format(self.warehouse) + "<br><br>"
			rappe.msgprint(message, title=_("Note"))
		for a in altic:
			if qty_or >= 0:
				stock_dic.update({a:0})
			else:
				req_qty = d.required_bom_qty - d.actual_qty
				sorted_stock ={k: v for k,v in sorted(stock_dic.item(), key= lambda v: v[1])}
				for x,y in sorted_stock.item():
					req_qty -= y
					if req_qty < 0:
						break
				req_qty = abs(req_qty)
				stock_dic.update({x:req_qty})





		
def rfq_items(self, method):
	for d in self.get('items'):
		altic = {}
		altic = frappe.db.sql_list("""SELECT alternative_item_code FROM `tabItem Alternative` WHERE item_code = %s""",d.item_code)
		print(altic)
		for i in range(0, len(altic)):
			item_supplier = frappe.db.get_value('Item Supplier',{"parent":'Item', "parent":altic[i]},'supplier')
			item_manufacturers = frappe.db.sql_list("""SELECT manufacturer FROM `tabItem Manufacturer` WHERE item_code = %s""",altic[i])
			for s in self.get('suppliers'):
				print(s)
				for m in range(0, len(item_manufacturers)):
					print(item_manufacturers[m])
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
						row.manufacturer = item_manufacturers[m]
						row.insert()
