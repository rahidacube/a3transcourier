frappe.ui.form.on('Delivery Note', {
	delivery_trip_receipt: function(frm) {

if (frm.doc.delivery_trip_receipt){
    frm.clear_table('items')
    frappe.call({
        method: "a3_ksrtc.a3_ksrtc.doc_events.delivery_note.get_data_from_receipt",
        args:{
            "trip_receipt": frm.doc.delivery_trip_receipt
        },
        callback: (r)=>{
            r.message.data.forEach((element)=>{
                const items = frm.add_child("items")
                    items.item_code = element.type_of_shipmentitem
                    items.item_name = element.type_of_shipmentitem
                    items.qty = 1
                    items.price_list_rate=element.price
                    items.rate = element.price
                    items.description=element.description
                    items.uom=element.stock_uom
                    items.warehouse=element.station
                    
                    refresh_field("items")
            })
        }
    })
}


    },

    close_delivery_note: function(doc){
		this.update_status("Closed")
	},

})