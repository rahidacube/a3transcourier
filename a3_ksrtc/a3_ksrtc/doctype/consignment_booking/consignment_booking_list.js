// frappe.listview_settings["Consignment Booking"] = {
//     onload: function(listview) {
//     const df = {
//         condition: "=",
//         default: null,
//         fieldname: "docstatus",
//         fieldtype: "Select",
//         input_class: "input-xs",
//         label: "DocStatus",
//         is_filter: 1,
//         onchange: function() {
//             listview.refresh();
//         },
//         options: [0,1,2],
//         placeholder: "DocStatus"
//     };

// //     //Add the filter to standard filter section
//     let standard_filters_wrapper = listview.page.page_form.find('.standard-filter-section');
//     listview.page.add_field(df, standard_filters_wrapper);

// //     //It will be a dropdown with options 1, 2, 3
// //     //To replace it with Blank space, Draft, Submitted and Cancelled.
// //     //First selecting the select option, may subject to changes as the the system
//     let doc_filter = document.querySelector('select[data-fieldname = "docstatus"]');

// //     //Add first option as blank space
//     doc_filter.options.add(new Option(), 0);

// //     //Changing just options’ inner html for better user experience
//     doc_filter.options[1].innerHTML = 'Draft';
//     doc_filter.options[2].innerHTML = 'Submitted';
//     doc_filter.options[3].innerHTML = 'Cancelled';
//     }
// }
// 
// frappe.listview_settings['Consignment Booking'] = {
//     onload(listview) {
//       // Triggers once before the list is loaded
//       listview.page.add_action_item('Create Lot', () => {
//         var selectedConsignments = listview.get_checked_items(true);
//         console.log(selectedConsignments);

//         frappe.prompt(
//           [
//             {
//               label: 'Destination Station',
//               fieldname: 'destination_station',
//               fieldtype: 'Link',
//               options: 'Warehouse',
//               reqd: 1
//             },
//             {
//                 label: 'Pickup Station',
//                 fieldname: 'pickup_station',
//                 fieldtype: 'Link',
//                 options: 'Warehouse',
//                 reqd: 1
//               },
//             {
//               label: 'Bag Number',
//               fieldname: 'bag_number',
//               fieldtype: 'Link',
//               options: 'Bag Number',
//               reqd: 1,
//               get_query: () => {
//                 return {
//                   filters: {
//                     status: 'Vacant'
//                   }
//                 };
//               }
//             }
//           ],
//           async (values) => {
//             frappe.call({
//                 method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.createlot",
//                 args:{
//                     "pickup_station": values.pickup_station,
//                     "destination_station": values.destination_station,
//                     "bag_number": values.bag_number,
//                     consignments: selectedConsignments
//                 },
           
//             callback: (r) => {
				
// 			}
//         });
            
//           },
//           'Create Lot'
//         ).set_primary_action('Submit', () => {
//           // Perform additional submit action, if required
//         });
//       });
//     }
//   };
frappe.listview_settings['Consignment Booking'] = {
    onload(listview) {
      // Triggers once before the list is loaded
      listview.page.add_action_item('Send Consignments', () => {
        var selectedConsignments = listview.get_checked_items(true);
        // user=frappe.session.user
        frappe.call({
            args:selectedConsignments,
            method:"a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.check_lotID",
        callback: (r)=>{
            if(r.message.hasLot){
                console.log(r.message.consignmentList)
                frappe.msgprint(__("One or more selected consignments already have a lot created."));
            }else{
                frappe.prompt(
                    [
                      {
                          label: 'Pickup Station',
                          fieldname: 'pickup_station',
                          fieldtype: 'Link',
                          options: 'Warehouse',
                          default:r.message.user_warehouse,
                          reqd: 1
                        },
                        {
                          label: 'Posting Date',
                          fieldname: 'date1',
                          fieldtype: 'Datetime',
                          reqd: 1,
                          default: frappe.datetime.now_datetime(),
                          read_only: 1 
                        },
                        {
                          label: 'Vehicle',
                          fieldname: 'vehicle',
                          fieldtype: 'Link',
                          options: 'Vehicle',
                          reqd: 1
                        },
                        {
                          label: 'Conductor',
                          fieldname: 'conductor',
                          fieldtype: 'Link',
                          options: 'Conductor',
                          reqd: 1,
                        },
                      
                      {
                          fieldname: 'col_break_1',
                          fieldtype: 'Column Break',
                        },
                        {
                          label: 'Destination Station',
                          fieldname: 'destination_station',
                          fieldtype: 'Link',
                          options: 'Warehouse',
                          reqd: 1
                        },
                        {
                          label: 'Bag Number',
                          fieldname: 'bag_number',
                          fieldtype: 'Link',
                          options: 'Bag Number',
                          reqd: 1,
                          get_query: () => {
                            return {
                              filters: {
                                status: 'Vacant'
                              }
                            };
                          }
                        },
                      
                        {
                          label: 'Driver',
                          fieldname: 'driver',
                          fieldtype: 'Link',
                          options: 'Driver',
                          reqd: 1
                        },
                        {
                        label: 'Make on Transit',
                        fieldname: 'on_Transit',
                        fieldtype: 'Check',
                        default: 0,
                        depends_on: 'eval:doc.driver && doc.vehicle && doc.conductor'
                        }
                       
                    ],
                    async (values) => {
                      console.log(values);
                      frappe.call({
                        method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.createlot",
                        args: {
                          "pickup_station": values.pickup_station,
                          "destination_station": values.destination_station,
                          "date1": values.date1,
                          "vehicle": values.vehicle,
                          "conductor": values.conductor,
                          "driver": values.driver,
                          "bag_number": values.bag_number,
                          "on_Transit": values.on_Transit,
                          consignments: selectedConsignments
                        },
                        callback: (r) => {
                          location.reload();
                          // frappe.ui.refresh("Consignment Booking");
                          // location.reload(); 
                          
                          
                          // Handle the response after creating the lot
                          // You can perform additional actions here if required
                        }
                      });
                    },
                    'Send Consignments'
                  ).set_primary_action('Submit', () => {
                     
                    // frappe.ui.refresh("Consignment Booking");
                    
                    // Perform additional submit action, if required
                  });
            }
        }})
     
        
      });
      listview.page.add_action_item('Receive Consignments', () => {
        var selectedConsignments = listview.get_checked_items(true);
        console.log(selectedConsignments);
        frappe.call({
            args:selectedConsignments,
            method:"a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.check_status",
        callback: (r)=>{
            if(r.message.hasLot){
                console.log(r.message.consignmentList)
                frappe.msgprint(__("The Selected consignments is not on transit."));
            }else{
                console.log(r.message.consignmentList)
                frappe.prompt(
                    [
                        {
                          label: 'Destination Station',
                          fieldname: 'destination_station',
                          fieldtype: 'Link',
                          options: 'Warehouse',
                          default:r.message.user_warehouse,
                          reqd: 1
                        },
                        {
                            label: 'LOT Number',
                            fieldname: 'lot_number',
                            fieldtype: 'Link',
                            options: 'LOT Number',
                            reqd: 1,
                            get_query: () => {
                              return {
                                filters: {
                                  end_station: r.message.user_warehouse,
                                }
                              };
                            }
                          },
                        {
                          label: 'Bag Number',
                          fieldname: 'bag_number',
                          fieldtype: 'Link',
                          options: 'Bag Number',
                          reqd: 1,
                          get_query: () => {
                            return {
                              filters: {
                                status: 'On-Transit',
                                destination: r.message.user_warehouse,
                              }
                            };
                          }
                        },
                      
                       
                    ],
                    async (values) => {
                      console.log(values);
                      frappe.call({
                        method: "a3_ksrtc.a3_ksrtc.doctype.consignment_booking.consignment_booking.create_delivery_receipt",
                        args: {
                          "destination_station": values.destination_station,
                          "bag_number": values.bag_number,
                          "consignments": selectedConsignments,
                          "lot_number": values.lot_number,
                        },
                        callback: (r) => {
                          location.reload();
                          // Handle the response after creating the lot
                          // You can perform additional actions here if required
                        }
                      });
                    },
                    'Receive Consignments'
                  ).set_primary_action('Submit', () => {
                    // location.reload();
                    // Perform additional submit action, if required
                  });
            }
        }})
     
        
      });
    }
  };