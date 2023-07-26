// Copyright (c) 2023, Acube and contributors
// For license information, please see license.txt

frappe.ui.form.on('LOT Number', {
    end_station: function(frm) {
        if(frm.doc.docstatus==0){
            frappe.call({
                method: "a3_ksrtc.a3_ksrtc.doctype.lot_number.lot_number.fetch_substaions",
                args:{
                    a:frm.doc.pickup_station,
                },
                callback: (r)=>{
					console.log("hiii",r.message)
					if(r.message){
						var list = r.message;
                    frm.add_custom_button(__('Booking'), function(){
                        erpnext.utils.map_current_doc({
                            method: "a3_ksrtc.a3_ksrtc.doc_events.sales_order.make_order_transfer",
                            source_doctype: "Sales Order",
                            target: frm,
                            date_field: "posting_date",
                            setters:
                            {
                                consignment_number:frm.doc.consignment_number,
                                // company: frm.doc.company,
                                customer:frm.doc.customer,
                                
                            },
                            
                            get_query_filters: {
                                docstatus: 1,
                                company: frm.doc.company,
                                pickup_station: ["in",r.message],
                                // dropoff_station: frm.doc.end_station,
                                consignment_status: ["in", ["Pending", "Arrived Mid Station"]]
            
        
                            }
                        })
                    }, "Get Consignment From")
                
                }
                
			}        
            })
        }

    }
});






frappe.ui.form.on('LOT Number', {
	onload: function(frm) {
		frm.clear_table("destinations")
		frm.set_query('bag_number', function() {
			return {
			  filters: {
				status: 'Vacant'
			  }
			};
		  });


		if(frm.doc.docstatus==0){
			frappe.call({
				method: "a3_ksrtc.a3_ksrtc.doctype.lot_number.lot_number.fetch_warehouse",
				args:{
					"user": frappe.session.user
				},
				callback: (r)=>{
					
					console.log("element",r.message)
						cur_frm.set_value("pickup_station",r.message.warehouse);
						frm.refresh_field('pickup_station');
						cur_frm.set_value("end_station",r.message.circle);
						frm.refresh_field('end_station');
					
						
				}
			})
		}
		
	}
})

