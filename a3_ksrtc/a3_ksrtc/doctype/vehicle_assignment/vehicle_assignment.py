# Copyright (c) 2023, Acube and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleAssignment(Document):
	def on_submit(self):
		if self.docstatus == 1:
			
			
			sharedoc = frappe.new_doc("DocShare")
			sharedoc.share_doctype="Vehicle Assignment"
			sharedoc.share_name=self.name
			us=frappe.get_doc("User Warehouse",{ "warehouse":self.end_point})
			print(us)
			sharedoc.user=us.user
			sharedoc.read=1
			sharedoc.write=1
			sharedoc.submit=1
			sharedoc.share=1
			sharedoc.notify=1
			sharedoc.save(ignore_permissions=True)
		for i in self.delivery_details:
			if i.order_transfer_lot:
				lot = frappe.get_doc("LOT Number", i.order_transfer_lot)
				for destinations in lot.destinations:
					if destinations.consignment_number:
						consignment_booking = frappe.get_doc("Consignment Booking", destinations.consignment_number)
						consignment_booking.vehicle_number = self.vehicle_
						consignment_booking.driver = self.driver
						consignment_booking.phone = self.driver_phone_number
						consignment_booking.conductor_name = self.condctor
						consignment_booking.conductors__phone_number = self.conductor_phone_number
					# Add vehicle history in consignment booking
						consignment_booking.append("vehicle_history",{
							"vehicle": self.vehicle_,
							"driver": self.driver,
							"conductor": self.condctor,
							"pick_up_station": self.start_point,
							"drop_off_station": self.end_point
						})
								
						consignment_booking.save(ignore_permissions=True)
			
				lot.vehicle = self.vehicle_
				lot.rtc_number = self.rt_number
				lot.vehicle_category = self.bus_category
				lot.driver = self.driver
				lot.driver_name = self.driver_name
				lot.driver_phone_number = self.driver_phone_number
				lot.conductor_n = self.condctor
				lot.conductor_name = self.conductor_name
				lot.conductor_email_ = self.conductor_phone_number
				# lot.transfer_status="Completed"
				lot.db_update()
				frappe.db.commit()
	def on_cancel(self):
		for i in self.delivery_details:
			if i.order_transfer_lot:
				lot=frappe.get_doc("LOT Number",i.order_transfer_lot)
				for destinations in lot.destinations:
					if destinations.consignment_number:
						consignment_booking = frappe.get_doc("Consignment Booking", destinations.consignment_number)
						consignment_booking.cstatus = "Pending"
						if consignment_booking.consignment_id:
									sal=frappe.get_doc("Sales Order",consignment_booking.consignment_id)
									sal.consignment_status="Pending"
									sal.save()
						consignment_booking.vehicle_number = ""
						consignment_booking.driver = ""
						consignment_booking.phone = ""
						consignment_booking.conductor_name = ""
						consignment_booking.conductors__phone_number= ""
						# consignment_booking.vehicle_history.clear()
						consignment_booking.db_update()
						frappe.db.commit()
						
				lot.vehicle = ""
				lot.rtc_number = ""
				lot.vehicle_category = ""
				lot.driver = ""
				lot.driver_name = ""
				lot.driver_phone_number = ""
				lot.conductor_n = ""
				lot.conductor_name = ""
				lot.conductor_email_ = ""
				lot.transfer_status="Pending"
				if lot.bag_number:
					bag=frappe.get_doc("Bag Number",lot.bag_number)
					bag.status="Destination Assigned"
					bag.save()
			
				

				lot.db_update()
				frappe.db.commit()
		




		
		mat=frappe.new_doc("Stock Entry")
		mat.purpose="Material Receipt"
		mat.stock_entry_type="Material Receipt"
		mat.vehicle_assignment=self.name
		
		for i in self.delivery_details:
			if i.order_transfer_lot:
				
				lot = frappe.get_doc("LOT Number", i.order_transfer_lot)
				lot.transfer_status="Pending"
				for destinations in lot.destinations:
					if destinations.delivery_note:
						sales_order = frappe.get_doc("Sales Order", destinations.delivery_note)
						sales_order.consignment_status = "Pending"
						consignment_booking = frappe.get_doc("Consignment Booking", destinations.consignment_number)
						consignment_booking.cstatus = "Pending"
						for item in sales_order.items:

							mat.append("items",{"t_warehouse":lot.pickup_station,
							"item_code":item.item_code,"qty":item.qty,"uom":item.uom,"rate":item.rate,"conversion_factor":item.conversion_factor,
							"stock_uom":item.stock_uom,"description":item.description,"item_name":item.item_name,"stock_qty":item.stock_qty,"allow_zero_valuation_rate":1
			


				})
						sales_order.save()
						consignment_booking.save()
				lot.save()
				

		mat.save(ignore_permissions=True)
		mat.submit()

		frappe.msgprint("Vehicle Cancelled")		
						
				
@frappe.whitelist(allow_guest=True)
def get_conductor(doc):
	data={}
	conductor=frappe.get_doc("Conductor",doc)
	if conductor.name:
		data["name"]=conductor.name
	if conductor.full_name:
		data["fname"]=conductor.full_name
	if conductor.cell_number:
		data["mobile"]=conductor.cell_number
	if conductor.address:
		data["address"]=conductor.address
	return data

@frappe.whitelist(allow_guest=True)
def get_driver(doc):
	driver=frappe.get_doc("Driver",doc)
	data={}
	if driver.cell_number:
		data["mobile1"]=driver.cell_number
	if driver.full_name:
		data["name"]=driver.full_name
	return data
@frappe.whitelist(allow_guest=True)
def get_vehicle(doc):
	if frappe.db.exists("Vehicle",{"rtc_number":doc}):
		vehicle=frappe.get_doc("Vehicle",{"rtc_number":doc})
		print(vehicle)
		data={}
		if vehicle.name:
			data["name"]=vehicle.name
		if vehicle.depot_name:
			data["depot"]=vehicle.depot_name
		if vehicle.engine_number:
			data["engine"]=vehicle.engine_number
		if vehicle.license_plate:
			data["license"]=vehicle.license_plate
		if vehicle.assigned_driver:
			dr=frappe.get_doc("Driver",vehicle.assigned_driver)
			if dr.cell_number:
				data["mobile"]=dr.cell_number
			if dr.full_name:
				data["named"]=dr.full_name
			data["driver"]=vehicle.assigned_driver
		if vehicle.assigned_conductor:
			cond=frappe.get_doc("Conductor",vehicle.assigned_conductor)
			if cond.cell_number:
				data["mobile1"]=cond.cell_number
			if cond.full_name:
				data["name1"]=cond.full_name
			data["conductor"]=vehicle.assigned_conductor
		return data
	else:
		return False

# @frappe.whitelist(allow_guest=True)
# def fetch_warehouse(user):
# 	user1=frappe.get_doc("User",user)
# 	userpermission=frappe.get_all("User Permission",filters={"user":user1.name},fields=["allow","for_value"])
# 	warehouse=[]
# 	for i in userpermission:
# 		if i.allow=="Warehouse":
# 			warehouse.append(i.for_value)
# 	return warehouse
@frappe.whitelist(allow_guest=True)
def fetch_warehouse(user):
	user1=frappe.get_doc("User",user)
	if frappe.db.exists("User Warehouse",{"user":user1.name}):
		data={}
		userper=frappe.get_doc("User Warehouse",{"user":user1.name})
		warehouse=userper.warehouse
		
		data["warehouse"]=warehouse
		if warehouse:
			war=frappe.get_doc("Warehouse",warehouse)
			if war.name_of_circle:
				data["circle"]=war.name_of_circle
		return data
	else:
		return False

@frappe.whitelist(allow_guest=True)
def create_stock_entry(**kwargs):
	print(kwargs["doc"])
	veh=frappe.get_doc("Vehicle Assignment",kwargs["doc"])
	mat=frappe.new_doc("Stock Entry")
	mat.purpose="Material Issue"
	mat.stock_entry_type="Material Issue"
	mat.vehicle_assignment=kwargs["doc"]
	
	for i in veh.delivery_details:

		if i.order_transfer_lot:
			
			lot = frappe.get_doc("LOT Number", i.order_transfer_lot)
			lot.transfer_status="On-Transit"
			if lot.bag_number:
				bag_number=frappe.get_doc("Bag Number",lot.bag_number)
				bag_number.status="On-Transit"
				bag_number.save()
			for destinations in lot.destinations:
				if destinations.delivery_note:
					sales_order = frappe.get_doc("Sales Order", destinations.delivery_note)
					consignment_booking=frappe.get_doc("Consignment Booking",destinations.consignment_number)
					consignment_booking.cstatus="On Transit"
					sales_order.consignment_status="On Transit"
					for item in sales_order.items:

						mat.append("items",{"s_warehouse":lot.pickup_station,"t_warehouse":lot.dropoff_station,
						"item_code":item.item_code,"qty":item.qty,"uom":item.uom,"rate":item.rate,"conversion_factor":item.conversion_factor,
						"stock_uom":item.stock_uom,"description":item.description,"item_name":item.item_name,"stock_qty":item.stock_qty,"allow_zero_valuation_rate":1
		


			})
					consignment_booking.db_update()
					frappe.db.commit()
					sales_order.db_update()
					frappe.db.commit()
			lot.db_update()
			frappe.db.commit()
	veh.vstatus="On Transit"
	veh.db_update()
	frappe.db.commit()
			

	mat.save(ignore_permissions=True)
	mat.submit()
	frappe.msgprint("Vehicle Transfered Successfully")
	return "success"
@frappe.whitelist(allow_guest=True)
def get_lot(bag):
	if frappe.db.exists("LOT Number",{"bag_number":bag}):
		lot=frappe.get_doc("LOT Number",{"bag_number":bag})
		if lot.transfer_status=="Pending":
			data={}
			if lot.name:
				data["name"]=lot.name
			if lot.pickup_station:
				data["pickup"]=lot.pickup_station
			if lot.end_station:
				data["dropoff"]=lot.end_station
		
			return data
	
		
	else:
		return False
