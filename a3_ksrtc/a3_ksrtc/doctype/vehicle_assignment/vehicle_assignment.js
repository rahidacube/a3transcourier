// Copyright (c) 2023, Acube and contributors
// For license information, please see license.txt
frappe.ui.form.on("Order Transfer Details", {


    bag_number: function(frm,cdt, cdn){

       
        console.log("Executing..")
       

            if (frm.doc.delivery_details){

                frm.doc.delivery_details.forEach(source_row => {


                 
					
                  
                    
        if (source_row.bag_number ){
            
					var bag=source_row.bag_number
					
            //primary
            frappe.call({
                
              // specify the server side method to be called.
              //dotted path to a whitelisted backend method
              method: "a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment.get_lot",
              //Passing variables as arguments with request
              args: {
                  bag:bag,
				  
                 
      
      
              },
            
              //Function passed as an argument to above function.
              callback: function(r) {
                  console.log(r.message.name,"###############")
                  
                    
                    {
                        //   const target_row=frm.add_child('items')
                         
                          source_row.order_transfer_lot =r.message.name;
                        
						source_row.pickup_station =r.message.pickup
						
						source_row.destination_station =r.message.dropoff
						frm.refresh_field('delivery_details');
            
                  }
                
            }
                  })

				}
		// else{
		// 	if (source_row.order_transfer_lot==null){ 
		// 	source_row.pickup_station =null;
		// 	source_row.destination_station =null;
		// 	frm.refresh_field('delivery_details');
		// 	}
		
		// }
                  })
                
                 
                
        
            }

}
    
    
    })

    

frappe.ui.form.on('Vehicle Assignment', {
	

	refresh: function(frm) {
		if(frm.doc.docstatus==1 && frm.doc.vstatus =="")
		{
		frm.add_custom_button(__("Make On-Transit"), function() {


			frappe.call({
				method: "a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment.create_stock_entry",
				args:{
					"doc": frm.doc.name,
					"company":frm.doc.company,
					"posting_date":frm.doc.date,
					"posting_time":frm.doc.time,
					"purpose":"Material Issue",
					"vehicle_assignment_id":frm.doc.name
				},

				callback: (r)=>{
				
					console.log(r.message)
					frm.set_value("vstatus", "On Transit");
					frm.refresh_field("vstatus")
					frm.reload_doc()
					
			
				}

			
			})
		
		})





	}
},
vstatus: function(frm) {
	if(frm.doc.vstatus=="On Transit" || frm.doc.vstatus=="Arrived Destination"){
		frm.remove_custom_button("Make On-Transit")
	};
},

condctor: function(frm) {
	if (frm.doc.condctor){
		frappe.call({
			method: "a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment.get_conductor",
			args:{
				"doc": frm.doc.condctor,
				
			},
			callback: (r)=>{
				
					console.log(r.message)
					
					cur_frm.set_value("conductor_name",r.message.fname)
					frm.refresh_field('conductor_name');
					cur_frm.set_value("conductor_phone_number",r.message.mobile)
					frm.refresh_field('conductor_phone_number');
					// cur_frm.set_value("conductor_address_",r.message.address)
					// frm.refresh_field('conductor_address_');
					
					
	
	
				
				
			}
		})
	
	}
	},
	driver: function(frm) {
		if (frm.doc.driver){
			frappe.call({
				method: "a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment.get_driver",
				args:{
					"doc": frm.doc.driver,
					
				},
				callback: (r)=>{
					
						console.log(r.message)
						cur_frm.set_value("driver_phone_number",r.message.mobile1)
						frm.refresh_field('driver_phone_number');
						
						cur_frm.set_value("driver_name",r.message.name)
						frm.refresh_field('driver_name');
						
		
		
					
					
				}
			})
		
		}
		},
	rt_number: function(frm) {
		
			// if (frm.doc.rt_number){
				frappe.call({
					method: "a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment.get_vehicle",
					args:{
						"doc": frm.doc.rt_number,
						
					},
					callback: (r)=>{
						
							console.log(r.message)
							cur_frm.set_value("vehicle_",r.message.name)
							frm.refresh_field('vehicle_');
							cur_frm.set_value("make_",r.message.depot)
							frm.refresh_field('make_');
							
							cur_frm.set_value("model",r.message.engine)
							frm.refresh_field('model');
							cur_frm.set_value("driver_phone_number",r.message.mobile)
							frm.refresh_field('driver_phone_number');
							
							cur_frm.set_value("driver_name",r.message.named)
							frm.refresh_field('driver_name');
							cur_frm.set_value("conductor_name",r.message.name1)
							frm.refresh_field('conductor_name');
							cur_frm.set_value("conductor_phone_number",r.message.mobile1)
							frm.refresh_field('conductor_phone_number');
							cur_frm.set_value("driver",r.message.driver)
							frm.refresh_field('driver');
							cur_frm.set_value("condctor",r.message.conductor)
							frm.refresh_field('condctor');

					}
				
				})
			
			// }
			// else{
			// 	cur_frm.set_value("vehicle_",null)
			// 	frm.refresh_field('vehicle_');
			// 	cur_frm.set_value("make_",null)
			// 	frm.refresh_field('make_');
			// 	cur_frm.set_value("model",null)
			// 	frm.refresh_field('model');
			// 	cur_frm.set_value("driver_phone_number",null)
			// 	frm.refresh_field('driver_phone_number');
			// 	cur_frm.set_value("driver_name",null)
			// 	frm.refresh_field('driver_name');
			// 	cur_frm.set_value("conductor_name",null)
			// 	frm.refresh_field('conductor_name');
			// 	cur_frm.set_value("conductor_phone_number",null)
			// 	frm.refresh_field('conductor_phone_number');
			// 	cur_frm.set_value("driver",null)
			// 	frm.refresh_field('driver');
			// 	cur_frm.set_value("condctor",null)
			// 	frm.refresh_field('condctor');		
			// }
			}	,

			

		
	
});





frappe.ui.form.on('Vehicle Assignment', {
	onload: function(frm) {

		cur_frm.fields_dict.delivery_details.grid.get_field("order_transfer_lot").get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
		
			return {
				filters: {
					"transfer_status": "Pending",
					"pickup_station": frm.doc.start_point,
					
				}
			 }
			};
			cur_frm.fields_dict.delivery_details.grid.get_field("bag_number").get_query = function(doc, cdt, cdn) {
				var child = locals[cdt][cdn];
			
				return {
					filters: {
						"status": "Destination Assigned",
						"pickup_station": frm.doc.start_point,
						
					}
				 }
				};
			
		if(frm.doc.docstatus==0){
			frm.clear_table('delivery_details')
			frappe.call({
				method: "a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment.fetch_warehouse",
				args:{
					"user": frappe.session.user
				},
				callback: (r)=>{
					console.log("element",r.message)
					
					cur_frm.set_value("start_point",r.message.warehouse);
					frm.refresh_field('start_point');
					cur_frm.set_value("end_point",r.message.circle);
					frm.refresh_field('end_point');
					const target_row=frm.add_child('delivery_details')
					target_row.pickup_station=r.message.warehouse
					frm.refresh_field('delivery_details');
				}
			})
		}
	}
})
