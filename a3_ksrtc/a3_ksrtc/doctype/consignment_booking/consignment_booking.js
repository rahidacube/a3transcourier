// Copyright (c) 2023, Acube and contributors
// For license information, please see license.txt
frappe.ui.form.on('Consignment Booking', {
	refresh: function(frm) {
		
		frm.set_df_property("full_name", "onchange", function() {
            var fullName = frm.doc.full_name;
            if (fullName.startsWith(" ")) {
                frm.set_value("full_name", fullName.trimStart());
            }
        });
		if (frm.doc.docstatus === 1) {
			frm.page.clear_secondary_action()
			frm.add_custom_button("Cancel",function(){
				frappe.confirm(
                    "Are you sure you want to cancel the Consignment Booking?",
                    function() {
                        // User clicked "Yes"
                        // Perform cancel operation
						// if (frm.doc.consignment_id){
                        frappe.call({
                            method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.cancel_booking",
                            args: {
                                consignment_id: frm.doc.consignment_id==null?"":frm.doc.consignment_id,
                                consignment_number: frm.doc.name,
                            },
                            callback: function(response) {
                                // Handle callback response if needed
                                frappe.msgprint("Booking canceled successfully.");
                            }
                        });
					// }
                    },
                    function() {
                        // User clicked "No"
                        // Do nothing or perform any other required action
                        frappe.msgprint("Cancellation canceled.");
                    }
                );
				// frappe.call({
				// 	method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.cancel_booking",
				// 	args:{
				// 		consignment_id:frm.doc.consignment_id,
				// 		consignment_number:frm.doc.name,
				// 	}
				// })
			});
			// frm.add_custom_button(__('Cancel'), function() {
			// 	cancelBooking(frm);
			// 	frappe.call({
            //         method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.send_otp",
            //         args: {
            //             receiver_number: receiverNumber,
            //             otp: otp,
			// 			val:val
            //         },
			// })
		}
			
		if(frm.is_new()){

			// frm.fields_dict["shipment_details"].grid.grid_buttons.find('.grid-buttons').addClass('hidden');
			$('*[data-fieldname="shipment_details"]').find('.grid-buttons').hide()
		}
		// frm.fields_dict["shipment_details"].grid.grid_buttons.find('.grid-add-row').addClass('hidden');
        if (frm.doc.docstatus == 1 && frm.doc.cstatus == 'Arrived Destination') {
            frm.add_custom_button(__('Create Delivery Note'), function() {
                var otp = Math.floor(100000 + Math.random() * 900000);
                var receiverNumber = frm.doc.phone_number;
				// var otp=123456
				var val=frm.doc.otp
				console.log(otp)

                // Send OTP using frappe.call
                frappe.call({
                    method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.send_otp",
                    args: {
                        receiver_number: receiverNumber,
                        otp: otp,
						val:val
                    },
                    callback: function(response) {
                        if (response && response.message) {
                            var enteredOTP = prompt('Enter the OTP received on your phone number');
                            if (enteredOTP && enteredOTP === otp.toString()) {
                                frappe.new_doc('Delivery Note', {
                                    'customer': frm.doc.full_name,
                                    'posting_date': frm.doc.date,
                                    'posting_time': frm.doc.time,
                                    'delivery_trip_receipt': frm.doc.name,
                                    'status': 'Closed'
                                });
                            } else {
                                frappe.msgprint('Incorrect OTP. Please try again.');
                            }
                        } else {
                            frappe.msgprint('Error sending OTP. Please try again.');
                        }
                    }
                });
            });
        }
    },



	cstatus: function(frm) {
		if(frm.doc.cstatus=="Delivered"){
			frm.remove_custom_button("Create Delivery Note");
		};
	},
	mobile_number: function(frm){
		
			
		frappe.call({
			method:"a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.fetch_customer_data",
			args: {
				// name: frm.doc.full_name,
				mobile_number: frm.doc.mobile_number,
			},
			callback: (r) => {
				console.log(r.message)
				cur_frm.set_value("full_name", r.message["customer_name"]);
				cur_frm.set_value("id_type", r.message["id_proof_type"]);
				cur_frm.set_value("id_number", r.message["id_proof_number"]);
				cur_frm.set_value("id_proof", r.message["attach_id"]);
				cur_frm.set_value("email", r.message["email"]);
				cur_frm.set_value("address_title", r.message["ad1"]);
				cur_frm.set_value("street_address", r.message["ad2"]);
				cur_frm.set_value("city", r.message["ad3"]);
				cur_frm.set_value("pin_code", r.message["pin"]);
				cur_frm.set_value("party_gstin", r.message["party_gstin"]);
				frm.refresh_field('party_gstin');
				frm.refresh_field('address_title');
				frm.refresh_field('street_address');
				frm.refresh_field('city');
				frm.refresh_field('pin_code');
				frm.refresh_field('email');
				frm.refresh_field('id_type');
				frm.refresh_field('full_name');
				frm.refresh_field('id_number');
				frm.refresh_field('id_proof');
			}
		})
	
	
	},
	phone_number: function(frm){
		
			console.log(frm.doc.is_sender,"kkkk")
			if (frm.doc.phone_number){
		frappe.call({
			method:"a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.fetch_receiver_data",
			args: {
				// name: frm.doc.full_name,
				mobile_number: frm.doc.phone_number,
			},
			callback: (r) => {
				console.log(r.message)
				cur_frm.set_value("name1", r.message["customer_name"]);
				cur_frm.set_value("type_of_id", r.message["id_proof_type"]);
				cur_frm.set_value("id_number1", r.message["id_proof_number"]);
				cur_frm.set_value("id_proof1", r.message["attach_id"]);
				cur_frm.set_value("email_id", r.message["email"]);
				cur_frm.set_value("address_line1", r.message["ad1"]);
				cur_frm.set_value("address_line_b", r.message["ad2"]);
				cur_frm.set_value("city1", r.message["ad3"]);
				cur_frm.set_value("pin_code1", r.message["pin"]);
				cur_frm.set_value("party_gstin", r.message["party_gstin"]);
				frm.refresh_field('party_gstin');
				frm.refresh_field('address_line1');
				frm.refresh_field('address_line_b');
				frm.refresh_field('city1');
				frm.refresh_field('pin_code1');
				frm.refresh_field('email_id');
				frm.refresh_field('type_of_id');
				frm.refresh_field('name1');
				frm.refresh_field('id_number1');
				frm.refresh_field('id_proof1');
			}
		})
		}
	}

});
frappe.ui.form.on("Shipment Details", {
	

	weight: function(frm,cdt, cdn){
		

	   
		console.log("Executing..")
		

			if (frm.doc.shipment_details){

				frm.doc.shipment_details.forEach(source_row => {
			if (source_row.weight && source_row.distance) {

					// var item=source_row.type_of_shipmentitem;
					var pickup=frm.doc.pickup_station;
					var dropoff=frm.doc.dropoff_station;
					var weight=source_row.weight;
					var distance=source_row.distance
					var box=frm.doc.is_box_size_above_75_cm;
					frappe.call({
						method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.fetch_item",
						args:{
							"weight": weight,
							"distance": distance,
							"box": box,
							"pickup_station": pickup,
							"dropoff_station": dropoff
						},
						callback: (r)=>{
							
							console.log("element",r.message)
							var wrate=r.message["rate"]
							var mweight=r.message["mweight"]
							var mdis=r.message["mdis"]
							var drate=r.message["drate"]
							var calc=r.message["val"]
							var kal=r.message["kal"]
							console.log(calc,"calc")
							console.log(kal,"kal")
							
							
							
				
				if (weight>1){
					console.log("weight",weight)
					console.log("distance",distance)
					if ((distance)>800){	
						let wt = Math.ceil(weight/mweight);
						console.log(wt,"1")
						var total=wt*drate
						console.log(total*distance)
						var new1=total*distance
						console.log(new1)
						var pricex=Math.round(distance*total)
						console.log(pricex)
						var x=pricex%5;
						var y=Math.floor(pricex/5);
						// console.log(x,y,"Test")
						if(x<=2.49){
							var z=(y)*5;
							var price1=z;
							source_row.total_cost_with_tax=z*1.18;
							source_row.price=z;
							// console.log(price1,"price1")

						}
						else{
							// console.log(y,"RAMIT")
							var z=(y+1)*5;
							// console.log(z,"SEBIN")
							source_row.total_cost_with_tax=z*1.18;
							source_row.price=z;
							var price1=z;
						}
						
						console.log(price1,"price 2")

						}

					else{
						if((distance)<=800){
						
						var dis=Math.ceil(distance/mdis)
						let wt = Math.ceil(weight/mweight);
						console.log(wt,"222")
						var total=wt*drate
						var dis1=dis*mdis
						var pricex=dis1*total

						var x=(pricex%5);
						var y=Math.floor(pricex/5);
						
						// console.log(x,y,"JOYEL")
						if(x<=2.49){
							console.log(x,y,"")
							var z=y*5;
							var price1=z;
							source_row.total_cost_with_tax=z*1.18;
							source_row.price=price1;
						// console.log(price1,"price3")
						}
						else{
							var z=(y+1)*5;
							var price1=z;
							source_row.total_cost_with_tax=z*1.18;
							source_row.price=price1;
						}
						
							
						console.log(price1,"price2")

					}
					}		
				}
				else if(weight<=1){
					if (frm.doc.is_box_size_above_75_cm){
						source_row.type_of_shipmentitem=r.message["item"]
						source_row.wrate=wrate
						var price1=(wrate)
						console.log(price1,"1")
						console.log(kal,"rrrrrrrrr")
						// source_row.price=price1;
						if(weight<=1){
						if (calc==0 && kal==0){
							source_row.price=wrate;
							source_row.total_cost_with_tax=wrate*1.18;
			
							
							}
						else{
							// console.log("eeeeeeee")
							var value=price1+(price1*.5);
								var rounded_val=Math.round(value);
								source_row.price=Math.round(value);
								source_row.total_cost_with_tax=rounded_val*1.18;
							
							}
						source_row.distance_rate=r.message["drate"]
						console.log(price1,drate,wrate)
						frm.refresh_field("shipment_details")
						cur_frm.set_value("cost",source_row.total_cost_with_tax);
						frm.refresh_field("cost");	
						
						}

					}
				
					else{
							var price1=(wrate)
							console.log(price1,"2")
						}
					}
							source_row.type_of_shipmentitem=r.message["item"]
							source_row.wrate=r.message["rate"]
							source_row.distance_rate=r.message["drate"]
							// source_row.price=price1;
							console.log(calc,kal)
							// source_row.price=price1;
							if (weight<=1){
								if (calc==0 && kal==0){
									source_row.price=wrate;
									source_row.total_cost_with_tax=wrate*1.18;
									
									}
								else{
									console.log(" this is the else part")
									var value1=price1+(price1*.5);
									var value_rounded=Math.round(value1);
									console.log(" this is the not else part")

									source_row.price=Math.round(value1);
									source_row.total_cost_with_tax=value_rounded*1.18;
									
									}
								}
							console.log(price1,drate,wrate)
							frm.refresh_field("shipment_details");
							cur_frm.set_value("cost",source_row.total_cost_with_tax);
							frm.refresh_field("cost");		
								
					
					
							
						}
					})
				}
	else{
							source_row.type_of_shipmentitem=""
							source_row.wrate=""
							source_row.distance_rate=""
							source_row.distance=""
							source_row.price="";
							frm.refresh_field("shipment_details");
							
	}
				})
			
			}
		}
		}),
					
					
					
					
		

frappe.ui.form.on('Consignment Booking', {
			onload: function(frm) {
				
				
				
				// // $('*[data-fieldname="shipment_details"]').find('.grid-add-row').hide()
				// frm.fields_dict["shipment_details"].grid.grid_buttons.find('.grid-add-row').addClass('hidden');
				// console.log("tttttttttttttt")
	

			
       

				if(frm.doc.docstatus==0){
				console.log("refreshing")
				console.log("refreshing11")
				cur_frm.set_value("created_user",frappe.session.user)
				frm.refresh_field('created_user');
				cur_frm.set_value("user",frappe.session.user)
				frm.refresh_field('user');
				cur_frm.set_value("date",frappe.datetime.get_today());
				frm.refresh_field('date');
				cur_frm.set_value("delivery_time",frappe.datetime.now_time());
				frm.refresh_field('delivery_time');
				cur_frm.set_value("delivery_date",frappe.datetime.get_today());;
				frm.refresh_field('delivery_date');
				}
				if (frappe.session.user!="Administrator"){
				if(frm.doc.docstatus==0){
					frappe.call({
						method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.fetch_warehouse",
						args:{
							"user": frappe.session.user
						},
						callback: (r)=>{
							
							console.log("element",r.message)
								cur_frm.set_value("pickup_station",r.message);
								frm.refresh_field('pickup_station');
								
							
						}
					})
				}
			}
		},
	

		})
frappe.ui.form.on('Consignment Booking', {
			is_sender: function(frm) {
				if (frm.doc.is_sender==1){
					cur_frm.set_value("name1",frm.doc.full_name);
					frm.refresh_field('name1');
					cur_frm.set_value("address_line1",frm.doc.address_title);
					frm.refresh_field('address_line1');
					cur_frm.set_value("address_line_b",frm.doc.street_address);
					frm.refresh_field('address_line_b');
					cur_frm.set_value("city1",frm.doc.city);
					frm.refresh_field('city1');
					cur_frm.set_value("pin_code1",frm.doc.pin_code);
					frm.refresh_field('pin_code1');
					cur_frm.set_value("type_of_id",frm.doc.id_type);
					frm.refresh_field('type_of_id');
					cur_frm.set_value("id_number1",frm.doc.id_number);
					frm.refresh_field('id_number1');
					cur_frm.set_value("id_proof1",frm.doc.id_proof);
					frm.refresh_field('id_proof1');

					cur_frm.set_value("phone_number",frm.doc.mobile_number);
					frm.refresh_field('phone_number');
					cur_frm.set_value("email_id",frm.doc.email);
					frm.refresh_field('email_id');

				}
				else{
					cur_frm.set_value("name1","");
					frm.refresh_field('name1');
					cur_frm.set_value("address_line1","");
					frm.refresh_field('address_line1');
					cur_frm.set_value("address_line_b","");
					frm.refresh_field('address_line_b');
					cur_frm.set_value("city1","");
					frm.refresh_field('city1');
					cur_frm.set_value("pin_code1","");
					frm.refresh_field('pin_code1');
					cur_frm.set_value("type_of_id","");
					frm.refresh_field('type_of_id');
					cur_frm.set_value("id_number1","");
					frm.refresh_field('id_number1');
					cur_frm.set_value("id_proof1","");
					frm.refresh_field('id_proof1');

					cur_frm.set_value("phone_number","");
					frm.refresh_field('phone_number');
					cur_frm.set_value("email_id","");
					frm.refresh_field('email_id');
				}
			},
		
		});
	
	frappe.ui.form.on("Shipment Details", {


		type_of_shipmentitem: function(frm,cdt, cdn){
			
			console.log("Executing..")
			if (frm.doc.shipment_details){
				frm.doc.shipment_details.forEach(source_row => {


					var item=source_row.type_of_shipmentitem;
					source_row.total_cost_with_tax=100
					

				frappe.model.with_doc('Item', item, function () {

					let ld = frappe.model.get_doc('Item',item);
					console.log(ld,"############")
					frappe.model.set_value(cdt, cdn, "wrate", ld.weight_rate);
					frappe.model.set_value(cdt, cdn, "rate", ld.per_squarefeet_rate);
					frappe.model.set_value(cdt, cdn, "distance_rate", ld.distance_rate);
					
				})
				frm.refresh_field('shipment_details');
				})

			
			}

		}
	});
	
	// Function to calculate the distance between two points using the Haversine formula
function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const earthRadius = 6371; // Radius of the Earth in kilometers

    // Convert latitude and longitude to radians
    const lat1Rad = toRadians(lat1);
    const lon1Rad = toRadians(lon1);
    const lat2Rad = toRadians(lat2);
    const lon2Rad = toRadians(lon2);

    // Calculate the differences between coordinates
    const latDiff = lat2Rad - lat1Rad;
    const lonDiff = lon2Rad - lon1Rad;

    // Apply the Haversine formula
    const a =
        Math.sin(latDiff / 2) ** 2 +
        Math.cos(lat1Rad) * Math.cos(lat2Rad) * Math.sin(lonDiff / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    // Calculate the distance
    const distance = earthRadius * c;
    return distance;
}

// Helper function to convert degrees to radians
function toRadians(degrees) {
    return (degrees * Math.PI) / 180;
}

frappe.ui.form.on('Consignment Booking', {
    dropoff_station: function(frm) {
        console.log("Executing dropoff_station function...");
		frm.clear_table("shipment_details");

        if (frm.doc.dropoff_station) {
            frappe.db.get_doc("Warehouse", frm.doc.pickup_station)
                .then(function(war1) {
                    frappe.db.get_doc("Warehouse", frm.doc.dropoff_station)
                        .then(function(war2) {
                            console.log(war1, "war1");
                            console.log(war2, "war2");
                            var distance1 = getDistanceFromLatLonInKm(war1.latitude, war1.longitude, war2.latitude, war2.longitude);
                            console.log(distance1, "distance");
                            cur_frm.set_value("distance", distance1);
							frm.refresh_field('distance');
                            
							const target_row=frm.add_child('shipment_details')
							target_row.distance =distance1
								frm.refresh_field('shipment_details')
								
                                
                            
                        });
                });
        }
    }
});

	

	// frappe.ui.form.on('Consignment Booking', {
	// 	on_submit: function(frm) {
	// 		frm.set_value("assign_to", "ramit.panangat@acube.co");
	// 	}
	// });
	