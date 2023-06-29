frappe.ui.form.on('Production Plan', {
	calculate_alternates:function(frm) {
	   
        const title = __("Transfer Materials For Warehouse {0}", [frm.doc.for_warehouse]);
			var dialog = new frappe.ui.Dialog({
				title: title,
				fields: [
					{
						'label': __('Source Warehouses (Optional)'),
						'fieldtype': 'Table MultiSelect',
						'fieldname': 'warehouses',
						'options': 'Production Plan Material Request Warehouse',
						'description': __('If source warehouse selected then system will create the material request with type Material Transfer from Source to Target warehouse. If not selected then will create the material request with type Purchase for the target warehouse.'),
						get_query: function () {
							return {
								filters: {
									company: frm.doc.company
								}
							};
						},
					},
				],
				primary_action(values) {
		var k = values.warehouses
					
					
					
      frm.set_value('alt_warehouses',JSON.stringify(k))
        dialog.hide();
    }
			});	
	    dialog.show();
	  
	}
})