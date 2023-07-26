# Copyright (c) 2023, Acube and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


	
class LOTNumber(Document):
	def validate(self):
		self.total_consignments = len(self.destinations)
		for i in self.destinations:
			i.consignment_no=i.consignment_number
			con_det=frappe.get_doc("Consignment Booking",i.consignment_number)
			print(con_det.phone_number,"tttttttttttttttttttttttttttttttttt")
			i.receiver_name=con_det.name1
			i.receiver_phone=con_det.phone_number
			i.sender_phone=con_det.mobile_number
					
	
	def after_insert(self):

		self.scan_lot=self.name
		self.save(ignore_permissions=True)
		for i in self.destinations:
			if i.delivery_note:
				sales_order = frappe.get_doc("Sales Order", i.delivery_note)
				print(sales_order)
				
				if sales_order.consignment_number:
					consignment_booking = frappe.get_doc("Consignment Booking", sales_order.consignment_number)
					if consignment_booking.cstatus=="Arrived Mid Station":
						if consignment_booking.vehicle_number:
							consignment_booking.vehicle_number=""
						if consignment_booking.driver:
							consignment_booking.driver = ""
						if consignment_booking.phone:
							consignment_booking.phone = ""
						if consignment_booking.conductor_name:
							consignment_booking.conductor_name = ""
						if consignment_booking.conductors__phone_number:
							consignment_booking.conductors__phone_number= ""
						consignment_booking.db_update()
						frappe.db.commit()
	def before_submit(self):
		for j in self.destinations:
			self.append("destination_table",{"customer":j.customer,"address":j.address,"sender_phone":j.sender_phone,"consignment_number":j.consignment_number,"receiver_name":j.receiver_name,"receiver_phone":j.receiver_phone,"delivery_note":j.delivery_note})
		# self.save(ignore_permissions=True)
		
	def on_submit(self):
		print(self.name,"name")
		if self.docstatus == 1:
		
			sharedoc = frappe.new_doc("DocShare")
			sharedoc.share_doctype="LOT Number"
			sharedoc.share_name=self.name
			us=frappe.get_doc("User Warehouse",{ "warehouse":self.end_station})
			
			sharedoc.user=us.user
			sharedoc.read=1
			sharedoc.write=1
			sharedoc.submit=1
			sharedoc.share=1
			sharedoc.notify=1
			sharedoc.save(ignore_permissions=True)
		# print(self.bag_number,"bagggggggg")
		for i in self.destinations:
			if i.consignment_number:
				consin=frappe.get_doc("Consignment Booking",i.consignment_number)
				# print(consin,"2323232332")
				consin.bag_number=self.bag_number
				# print(consin.bag_number,"22222222222222")
				consin.save()
				consin.db_update()
			# frappe.db.update(consin)
		frappe.db.commit()

		if self.bag_number:
			bag = frappe.get_doc("Bag Number", self.bag_number)
			bag.status = "Destination Assigned"
			bag.destination=self.end_station
			bag.pickup_station=self.pickup_station
			bag.save(ignore_permissions=True)
			# bag.db_update()
			# frappe.db.commit()
		for i in self.destinations:
			if i.delivery_note:
				sales_order = frappe.get_doc("Sales Order", i.delivery_note)
				print(sales_order)
				
				if sales_order.consignment_number:
					consignment_booking = frappe.get_doc("Consignment Booking", sales_order.consignment_number)
					
					print(consignment_booking)

					consignment_booking.lot_id = self.name
					# consignment_booking.cstatus = "On Transit"
					
					if consignment_booking.cstatus=="Arrived Mid Station":
						if consignment_booking.lot_id=="":
							consignment_booking.lot_id = self.name
							
					consignment_booking.db_update()
					frappe.db.commit()
					if consignment_booking.dropoff_station != self.end_station:
						print("in if")
						sharedoc = frappe.new_doc("DocShare")
						sharedoc.share_doctype="Consignment Booking"
						sharedoc.share_name=consignment_booking.name
						us=frappe.get_doc("User Warehouse",{ "warehouse":self.end_station})
						print(us)
						sharedoc.user=us.user
						sharedoc.read=1
						sharedoc.write=1
						sharedoc.submit=1
						sharedoc.share=1
						sharedoc.notify=1
						sharedoc.save(ignore_permissions=True)
	def on_cancel(self):
		if self.bag_number:
			bag = frappe.get_doc("Bag Number", self.bag_number)
			bag.status = "Vacant"
			bag.destination=""
			bag.pickup_station=""
			bag.save(ignore_permissions=True)
		for i in self.destinations:
			if i.delivery_note:
				sales_order = frappe.get_doc("Sales Order", i.delivery_note)
				
				
				if sales_order.consignment_number:
					consignment_booking = frappe.get_doc("Consignment Booking", sales_order.consignment_number)
					consignment_booking.lot_id = ""
					consignment_booking.db_update()
					frappe.db.commit()					

							



@frappe.whitelist(allow_guest=True)
def fetch_warehouse(user):
	user1=frappe.get_doc("User",user)
	print(user1)
	data = {}
	if frappe.db.exists("User Warehouse",{"user":user1.name}):
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
def fetch_substaions(a):
	s=[]
	print(a)
	s.append(a)
	if frappe.db.exists("Warehouse",{"name_of_circle":a}):
		list=frappe.db.get_list("Warehouse",{"name_of_circle":a})
		print(list)
		for i in list:
			print(i.name)
			s.append(i.name)
			print(s)

		return s
	else:
		
		return s