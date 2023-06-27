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
					for (var i =0;i<values.warehouses.lenght;i++){
					    
					}
					console.log(values.warehouses[0])
      frappe.call({
          method:"microconsultant.microconsultant.rfq_development.add_items",
          args:{doc:frm.doc.name,warehouse:values.warehouses}
      })
        dialog.hide();
    }
			});	
	    dialog.show();
	  
	}
})