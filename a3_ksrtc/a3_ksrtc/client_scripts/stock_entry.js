

frappe.ui.form.on('Stock Entry', {
	refresh: function(frm) {
        frm.add_custom_button(__("Sales Order"), function() {
            frappe.call(
                {
                    method: "a3_ksrtc.a3_ksrtc.doc_events.stock_entry.fetch_items",
                    args:{
                        "orderform": frm.doc.vehicle_assignment_id
                    },
                    callback:(r)=>{
                        frm.clear_table("items")
                        r.message.data.forEach(element => {
                        
                            const items = frm.add_child("items")
                            items.s_warehouse=element.s_warehouse
                            items.t_warehouse=element.t_warehouse
                            items.item_code = element.item_code
                            items.qty = element.qty
                            items.conversion_factor = element.conversion_factor
                            items.transfer_qty = element.stock_qty
					        refresh_field("items")
                        });
                    }
                }
            )
    
        }, __('Get Items From'));
}
});


