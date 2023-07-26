// Copyright (c) 2023, Acube and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Trip Receipt', {
	
	

	onload: function(frm) {
		cur_frm.fields_dict['consignment_number'].get_query = function(doc) {
			return {
			
					filters: frm.doc.lot_destination?[["end_station","=",frm.doc.lot_destination],["transfer_status","=","On-Transit"]]:[],
					
			
			 }
			};
			cur_frm.fields_dict['bag_number'].get_query = function(doc) {
				return {
				
						filters: frm.doc.lot_destination?[["destination","=",frm.doc.lot_destination],["status","=","On-Transit"]]:[],
						
				
				 }
				};


		
		frappe.call({
			method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.fetch_warehouse",
			args:{
				"user": frappe.session.user
			},
			callback: (r)=>{
				console.log("hiii",r.message)
				if(r.message){
					if(frappe.session.user!="Administrator"){
					cur_frm.set_value("dropoff_station",r.message);
					frm.refresh_field('dropoff_station');
					cur_frm.set_value("lot_destination",r.message);
					frm.refresh_field('lot_destination');
					}
				
				} 
				else {
					if (frappe.session.user!="Administrator"){
					frappe.throw("No Station assigned for this user.")
					}
				}
			}
		})
		
	},

consignment_number: function(frm){


frm.clear_table("consignment_list")
if(frappe.session.user!="Administrator"){
		if(frm.doc.lot_destination == frm.doc.dropoff_station){
			if(frm.doc.consignment_number){
				frappe.call({
					method: "a3_ksrtc.a3_ksrtc.doctype.delivery_trip_receipt.events.fetch_consignment",
					args:{
						lot_number: frm.doc.consignment_number
					},
					callback: (r) => {
						console.log(r.message)
						r.message.forEach((element)=>{
							console.log(r.message)
							clear_table("consignment_list")

						
					

							frm.doc.dropoff_station = frm.doc.lot_destination
							refresh_field("dropoff_station")
							frm.doc.delivery_date = element.delivery_date
							refresh_field("delivery_date")
							frm.doc.delivery_time = element.delivery_time
							frm.doc.bag_number = element.bag_number
							refresh_field("bag_number")
							refresh_field("delivery_time")
							const consignment_list = frm.add_child("consignment_list")
							consignment_list.consignment = element.consignment_id
							consignment_list.customer_name = element.customer_name
							consignment_list.customer_phone_number = element.customer_phone
							consignment_list.receiver_name = element.receiver_name
							consignment_list.receiver_phone_number = element.receiver_phone
							refresh_field("consignment_list")
						



							

						})
					}
				})
			}
		}
else{
			
			frappe.throw("This LOT's destination is not here")
			
		}
	}


	if(frappe.session.user=="Administrator"){
		
			if(frm.doc.consignment_number){
				frappe.call({
					method: "a3_ksrtc.a3_ksrtc.doctype.delivery_trip_receipt.events.fetch_consignment",
					args:{
						lot_number: frm.doc.consignment_number
					},
					callback: (r) => {
						r.message.forEach((element)=>{
							frm.doc.dropoff_station = frm.doc.lot_destination
							refresh_field("dropoff_station")
							frm.doc.delivery_date = element.delivery_date
							refresh_field("delivery_date")
							frm.doc.delivery_time = element.delivery_time
							refresh_field("delivery_time")
							frm.doc.bag_number = element.bag_number
							refresh_field("bag_number")
							const consignment_list = frm.add_child("consignment_list")
							consignment_list.consignment = element.consignment_id
							consignment_list.customer_name = element.customer_name
							consignment_list.customer_phone_number = element.customer_phone
							consignment_list.receiver_name = element.receiver_name
							consignment_list.receiver_phone_number = element.receiver_phone
							refresh_field("consignment_list")



							

						})
					}
				})
			}
		}
		



	},







// 
bag_number: function(frm){


							if(frm.doc.bag_number){
					frappe.call({
						method: "a3_ksrtc.a3_ksrtc.doctype.delivery_trip_receipt.events.fetch_lot",
						args:{
							bag: frm.doc.bag_number
						},
						callback: (r) => {
							console.log("hiii",r.message)
						cur_frm.set_value("consignment_number", r.message.name);
						frm.refresh_field("consignment_number");
						}
					})
				
			
			
		}
	
	
	
		}




});
