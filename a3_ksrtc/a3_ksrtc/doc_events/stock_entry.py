import frappe

@frappe.whitelist()
def fetch_items(orderform):
	items = []
	orderID = frappe.get_doc("Vehicle Assignment", orderform)
	for i in orderID.delivery_details:
		if i.order_transfer_lot:
			data = {}
			lot = frappe.get_doc("LOT Number", i.order_transfer_lot)
			data["s_warehouse"]=lot.pickup_station
			data["t_warehouse"]=lot.dropoff_station
			for destinations in lot.destinations:
				if destinations.delivery_note:
					sales_order = frappe.get_doc("Sales Order", destinations.delivery_note)
					for item in sales_order.items:
						
						data["item_code"] = item.item_code
						data["item_name"] = item.item_name
						data["stock_qty"] = item.stock_qty
						data["conversion_factor"] = item.conversion_factor
						data["qty"] = item.qty
						items.append(data)
	
	return {"data":items}

# def on_submit(doc,method):
# 	if doc.stock_entry_type == "Material Issue":
# 		if doc.vehicle_assignment_id:
# 			orderID = frappe.get_doc("Vehicle Assignment", doc.vehicle_assignment_id)
# 			for i in orderID.delivery_details:
# 				if i.order_transfer_lot:
# 					lot=frappe.get_doc("LOT Number",i.order_transfer_lot)
# 					print(lot)
# 					for destinations in lot.destinations:
# 						if destinations.delivery_note:
# 							sales_order = frappe.get_doc("Sales Order", destinations.delivery_note)
# 							print(sales_order)
# 							if sales_order.consignment_number:
# 								consignment_booking = frappe.get_doc("Consignment Booking", sales_order.consignment_number)
# 								print(consignment_booking)
# 								consignment_booking.status = "On Transit"
# 								if consignment_booking.consignment_id:
# 									sal=frappe.get_doc("Sales Order",consignment_booking.consignment_id)
# 									sal.consignment_status="On Transit"
# 									sal.save()
# 								consignment_booking.save()









		