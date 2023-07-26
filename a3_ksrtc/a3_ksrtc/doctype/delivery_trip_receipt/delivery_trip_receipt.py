# Copyright (c) 2023, Acube and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DeliveryTripReceipt(Document):
	def after_insert(self):
		for shipment in self.consignment_list:
			consignment = frappe.get_doc("Consignment Booking", shipment.consignment)
			stock=frappe.new_doc("Stock Entry")
			stock.stock_entry_type = "Material Receipt"
			
			for consign in consignment.shipment_details:
				stock.append("items",{"item_code":consign.type_of_shipmentitem,"qty":consign.quantity,"t_warehouse":self.dropoff_station, "allow_zero_valuation_rate":1})		
			stock.save()
			stock.submit()

	def before_submit(self):
		for consign in self.consignment_list:
			consignment_booking = frappe.get_doc("Consignment Booking", consign.consignment)
			user=frappe.session.user
			if consignment_booking.lot_id:
				lot=frappe.get_doc("LOT Number",consignment_booking.lot_id)
				if lot.bag_number:
					bag=frappe.get_doc("Bag Number",lot.bag_number)
					bag.status="Vacant"
					bag.destination=""
					bag.pickup_station=""
					bag.save()
			if frappe.session.user!="Administrator":
				user_war=frappe.get_doc("User Warehouse",{"user":user})
				if user_war.warehouse==consignment_booking.dropoff_station:
					consignment_booking.cstatus = "Arrived Destination"
					consignment_booking.save()
					if consignment_booking.lot_id:
						lot=frappe.get_doc("LOT Number",consignment_booking.lot_id)
						
						print(lot)
						lot.transfer_status="Arrived"
						lot.db_update()
						frappe.db.commit()
						
					if consignment_booking.consignment_id:
						sal=frappe.get_doc("Sales Order",consignment_booking.consignment_id)
						
						sal.consignment_status="Arrived Destination"
						sal.db_update()
						frappe.db.commit()
					consignment_booking.db_update()
					frappe.db.commit()
				
				else:
					consignment_booking.cstatus = "Arrived Mid Station"
					lot=frappe.get_doc("LOT Number",consignment_booking.lot_id)
					lot.transfer_status="Arrived"
					lot.db_update()
					frappe.db.commit()
			
					if consignment_booking.consignment_id:
						sal=frappe.get_doc("Sales Order",consignment_booking.consignment_id)
						
						sal.consignment_status="Arrived Mid Station"
						sal.db_update()
						frappe.db.commit()
					consignment_booking.save()
				if consignment_booking.vehicle_number:
					va = frappe.get_doc("Vehicle Assignment",{"vehicle_":consignment_booking.vehicle_number})
					va.status = "Arrived Destination"
					va.db_update()
					frappe.db.commit()
	def on_submit(self):
		# for shipment in self.consignment_list:
		# 	consignment = frappe.get_doc("Consignment Booking", shipment.consignment)
		# 	stock=frappe.new_doc("Stock Entry")
		# 	stock.stock_entry_type = "Material Receipt"
			
		# 	for consign in consignment.shipment_details:
		# 		stock.append("items",{"item_code":consign.type_of_shipmentitem,"qty":consign.quantity,"t_warehouse":self.dropoff_station, "allow_zero_valuation_rate":1})		
		# 	print(self.dropoff_station)
		# 	stock.save()
		# 	stock.submit()
		
		for consign in self.consignment_list:
			consignment_booking = frappe.get_doc("Consignment Booking", consign.consignment)
			user=frappe.session.user
			if frappe.session.user!="Administrator":
				user_war=frappe.get_doc("User Warehouse",{"user":user})
				if user_war.warehouse!=consignment_booking.dropoff_station:
					if consignment_booking.lot_id:
						if consignment_booking.lot_id:
							consignment_booking.lot_id=""
		
			if consignment_booking.consignment_id:
				sal=frappe.get_doc("Sales Order",consignment_booking.consignment_id)
				
				sal.pickup_station=self.lot_destination
				sal.db_update()
				frappe.db.commit()
	def on_cancel(self):
		get_bag_number=frappe.get_doc("Bag Number",self.bag_number)
		get_bag_number.status="On-Transit"
		get_bag_number.save()




	