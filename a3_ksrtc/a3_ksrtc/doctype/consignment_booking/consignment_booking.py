# Copyright (c) 2023, Acube and contributors
# For license information, please see license.txt

import frappe
from a3_ksrtc.a3_ksrtc.doctype.vehicle_assignment.vehicle_assignment import create_stock_entry
from datetime import date
import re
from frappe.model.document import Document
from a3_ksrtc.a3_ksrtc.attach_pdf import attach_pdf
import random
import string
class ConsignmentBooking(Document):
	def after_insert(self):
		self.scan_consignment=self.name
		# print(frappe.session.user)
		# print(self.owner)
		# self.user=frappe.session.user
		# self.created_user=self.owner
		self.save(ignore_permissions=True)
		print(self.user)
	
	
	def validate(self):
			if self.mobile_number:
				r=re.fullmatch('[6-9][0-9]{9}',self.mobile_number)
				if r!=None:
					pass

				else:
					frappe.throw("Please Check your Mobile Number ")
			if self.id_type=="PAN Card":
				if self.id_number:
					r=re.fullmatch('[A-Z]{5}[0-9]{4}[A-Z]{1}',self.id_number)
					if r!=None:
						pass
					else:
						frappe.throw("Please Check your PAN Card Number ")
			# if self.id_type=="Driving License":
			# 	if self.id_number:
			# 		r=re.fullmatch('[A-Z]{2}[0-9]{2}[0-9]{11}',self.id_number)
			# 		if r!=None:
			# 			pass
			# 		else:
			# 			frappe.throw("Please Check your Driving License Number ")
			if self.id_type=="Aadhaar Card":
				if self.id_number:
					r=re.fullmatch('[0-9]{12}',self.id_number)
					if r!=None:
						pass
					else:
						frappe.throw("Please Check your Aadhaar Card Number ")
			if self.email:
				r=re.fullmatch('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',self.email)
				if r!=None:
					pass
				else:
					frappe.throw("Please Check your Email ")
			if self.email_id:
				r=re.fullmatch('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',self.email_id)
				if r!=None:
					pass
				else:
					frappe.throw("Please Check Receiver's Email ")
			if self.phone_number:
				r=re.fullmatch('[6-9][0-9]{9}',self.phone_number)
				if r!=None:
					pass
				else:
					frappe.throw("Please Check  Receiver's Mobile Number ")
			if self.type_of_id=="PAN Card":
				if self.id_number1:
					r=re.fullmatch('[A-Z]{5}[0-9]{4}[A-Z]{1}',self.id_number1)
					if r!=None:
						pass
					else:
						frappe.throw("Please Check Receiver's PAN Card Number ")
			# if self.type_of_id=="Driving License":
			# 	if self.id_number1:
			# 		r=re.fullmatch('[A-Z]{2}[0-9]{2}[0-9]{11}',self.id_number1)
			# 		if r!=None:
			# 			pass
			# 		else:
			# 			frappe.throw("Please Check Receiver's Driving License Number ")
			if self.type_of_id=="Aadhaar Card":
				if self.id_number1:
					r=re.fullmatch('[0-9]{12}',self.id_number1)
					if r!=None:
						pass
					else:
						frappe.throw("Please Check Receiver's Aadhaar Card Number ")
			# if self.party_gstin:
			# 	r=re.fullmatch('[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[0-9]{1}',self.party_gstin)
			# 	if r!=None:
			# 		pass
			# 	else:
			# 		frappe.throw("Please Check GSTIN Number ")
			
			
		
				
			if self.pickup_station:
				pickup=frappe.get_doc("Warehouse",self.pickup_station)
				x=pickup.station_code1
			if self.dropoff_station:
				dropoff=frappe.get_doc("Warehouse",self.dropoff_station)
				y=dropoff.station_code1
			self.location_code=x+"-"+y
			if self.allow==0:
				self.delivery_date=date.today()
				self.allow=1

		
	
	def on_submit(self):
		if self.docstatus == 1:
			# if self.sales_invoice:
			sharedoc = frappe.new_doc("DocShare")
			sharedoc.share_doctype="Consignment Booking"
			sharedoc.share_name=self.name
			if frappe.db.exists("User Warehouse",{ "warehouse":self.dropoff_station}):
				us=frappe.get_doc("User Warehouse",{ "warehouse":self.dropoff_station})
				# print(us,"ttttttttttttttttttttttttttttttttttttttttttttttttttttt")
				sharedoc.user=us.user
				sharedoc.read=1
				sharedoc.write=1
				sharedoc.submit=1
				sharedoc.share=1
				sharedoc.notify=1
				sharedoc.report=1
				sharedoc.save(ignore_permissions=True)
			else:
				frappe.throw("There is no user exists in destination station")
			sharedoc = frappe.new_doc("DocShare")
			sharedoc.share_doctype="Consignment Booking"
			sharedoc.share_name=self.name
			sharedoc.user=self.owner
			sharedoc.read=1
			sharedoc.write=1
			sharedoc.submit=1
			sharedoc.share=1
			sharedoc.notify=1
			sharedoc.report=1
			sharedoc.save(ignore_permissions=True)
			print(self.owner)
			# if not frappe.db.exists("User Permission",{"user":self.owner,"allow":"Consignment Booking"}):
			
			# 	up=frappe.new_doc("User Permission")
			# 	up.user=self.owner
			# 	up.allow="Consignment Booking"
			# 	up.for_value=self.name
			# 	up.save(ignore_permissions=True)
					
			domain = "example.com" 
			username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
			remail = f"{username}@{domain}"

			if self.full_name:
				
				# Create sender customer and user
				if not frappe.db.exists("Customer", {"customer_name":self.full_name,"mobile_number":self.mobile_number}):
					if frappe.db.exists("Customer", {"mobile_number":self.mobile_number}):
						frappe.throw("Sender's mobile number is already registered with other customer.")
					else:
						customer = frappe.new_doc("Customer")
						customer.customer_name = self.full_name
						customer.territory = "India"
						customer.customer_group = "Individual"
						customer.id_proof_type = self.id_type
						customer.id_proof_number = self.id_number
						customer.attach_id=self.id_proof
						if self.address_title:
							customer.ad1=self.address_title
						if self.street_address:
							customer.ad2=self.street_address
						if self.city:
							customer.ad3=self.city
						if self.pin_code:
							customer.pin=self.pin_code
						if self.gst_state1=="Kerala":
							customer.tax_category="In-State"
						else:
							customer.tax_category="Out-State"
						if self.gst_state1:
							customer.state=self.gst_state1
						if self.party_gstin:
							customer.party_gstin=self.party_gstin
						if self.email:
							customer.email=self.email
						else:
							self.email=remail
							customer.email=remail

						customer.mobile_number=self.mobile_number
						customer.save()
				if frappe.db.exists("Customer", {"customer_name":self.full_name,"mobile_number":self.mobile_number}):
					customer=frappe.get_doc("Customer",{"customer_name":self.full_name,"mobile_number":self.mobile_number})
					if not customer.party_gstin:
						# frappe.throw("Sender's mobile number is already registered with other customer.")

						if self.party_gstin:
							customer.party_gstin=self.party_gstin
							customer.save()
				# Create receiver customer and user
				if not frappe.db.exists("Customer", {"customer_name":self.name1,"mobile_number":self.phone_number}):
					if frappe.db.exists("Customer", {"mobile_number":self.phone_number}):
						frappe.throw(f"Receiver's mobile number is already registered with other customer.")
					else:
						customer = frappe.new_doc("Customer")
						customer.customer_name = self.name1
						customer.territory = "India"
						customer.customer_group = "Individual"
						customer.id_proof_type = self.type_of_id
						customer.id_proof_number = self.id_number1
						customer.attach_id=self.id_proof1
						customer.ad1=self.address_line1
						customer.ad2=self.address_line_b
						customer.ad3=self.city1
						customer.pin=self.pin_code1
						if self.email_id:
							customer.email=self.email_id
					
						
						customer.mobile_number=self.phone_number
						customer.save()
					
				sal=frappe.new_doc("Sales Order")
				
				sal.customer = self.full_name
				sal.customer_name = self.full_name
				
				sal.consignment_number=self.name
				sal.pickup_station=self.pickup_station
				sal.dropoff_station=self.dropoff_station
				sal.consignment_status="Pending"
				sal.delivery_date = frappe.utils.nowdate()
				if self.gst_state1=="Kerala":
					sal.tax_category="In-State"
					for j in self.shipment_details:
						sal.append("items",{"item_code":j.type_of_shipmentitem,"qty":1,"rate":j.price,"warehouse":self.dropoff_station})
						# sal.tax_category="In-State"
						item=frappe.get_doc("Item",j.type_of_shipmentitem)

						saltx=frappe.get_doc("Sales Taxes and Charges Template",{ "tax_category":"In-State"})
						sal.taxes_and_charges=saltx.name
						for tax in saltx.taxes:
							x=tax.account_head
							y=tax.rate
							sal.append("taxes",{"charge_type":"On Net Total","account_head":x,"rate":y,"description":"Tax"})
				else: 
					sal.tax_category="Out-State"
					for j in self.shipment_details:
						sal.append("items",{"item_code":j.type_of_shipmentitem,"qty":1,"rate":j.price,"warehouse":self.dropoff_station})
						# sal.tax_category="In-State"
						item=frappe.get_doc("Item",j.type_of_shipmentitem)

						saltx=frappe.get_doc("Sales Taxes and Charges Template",{ "tax_category":"Out-State"})
						sal.taxes_and_charges=saltx.name
						for tax in saltx.taxes:
							x=tax.account_head
							y=tax.rate
							sal.append("taxes",{"charge_type":"On Net Total","account_head":x,"rate":y,"description":"Tax"})
						
						
				sal.insert()
				
				sal.submit()
				self.consignment_id=sal.name
				# self.cost=sal.total
				# self.total_taxes_and_charges=sal.total_taxes_and_charges
				self.save()
			
				
				stock=frappe.new_doc("Stock Entry")
				stock.stock_entry_type = "Material Receipt"
				
				for j in self.shipment_details:
					stock.append("items",{"item_code":j.type_of_shipmentitem,"qty":1,"t_warehouse":self.pickup_station, "allow_zero_valuation_rate":1})		
				stock.save()
				stock.submit()
				
				if not self.sales_invoice:
					sinv=frappe.new_doc("Sales Invoice")
					sinv.customer = self.full_name
					sinv.customer_name = self.full_name
					if self.gst_state1=="Kerala":
						for j in self.shipment_details:
							sinv.append("items",{"item_code":j.type_of_shipmentitem,"qty":1,"rate":j.price,"warehouse":self.dropoff_station})
							item=frappe.get_doc("Item",self.shipment_details[0].type_of_shipmentitem)
							saltx=frappe.get_doc("Sales Taxes and Charges Template",{ "tax_category":"In-State"})
							sinv.taxes_and_charges=saltx.name
							for tax in saltx.taxes:
								x=tax.account_head
								y=tax.rate
								sinv.append("taxes",{"charge_type":"On Net Total","account_head":x,"rate":y,"description":"Tax"})
					else:
						for j in self.shipment_details:
							sinv.append("items",{"item_code":j.type_of_shipmentitem,"qty":1,"rate":j.price,"warehouse":self.dropoff_station})
							item=frappe.get_doc("Item",self.shipment_details[0].type_of_shipmentitem)
							saltx=frappe.get_doc("Sales Taxes and Charges Template",{ "tax_category":"Out-State"})
							sinv.taxes_and_charges=saltx.name
							for tax in saltx.taxes:
								x=tax.account_head
								y=tax.rate
								sinv.append("taxes",{"charge_type":"On Net Total","account_head":x,"rate":y,"description":"Tax"})
					
									
					sinv.insert()
					sinv.submit()

					self.sales_invoice = sinv.name
					self.save()
				payment=frappe.new_doc("Payment Entry")
				payment.party_type="Customer"
				payment.party=self.full_name
				payment.party_name=self.full_name
				if sal.company:
					com=frappe.get_doc("Company",sal.company)
					print(com)
					payment.paid_from=com.default_receivable_account
					payment.paid_to=com.default_cash_account
			payment.paid_to_account_currency="INR"
			payment.paid_from_account_currency="INR"
			payment.payment_type="Receive"
			payment.mode_of_payment="Cash"	
			current_date=frappe.utils.nowdate()			
			payment.reference_date=current_date
			payment.total_allocated_amount=self.cost
			payment.paid_amount=self.cost
			payment.received_amount=self.cost
			
			payment.append("references",{"reference_doctype":"Sales Invoice","reference_name":self.sales_invoice,"total_amount":self.cost,"allocated_amount":self.cost,"outstanding_amount":self.cost})
			payment.insert()
			# "outstanding_amount":self.cost,
			
			payment.submit()




	def before_insert(self):
			if self.pickup_station:
				pickup=frappe.get_doc("Warehouse",self.pickup_station)
				if pickup.station_code:
					self.pickup_code=pickup.station_code
							
			if self.dropoff_station:
				dropoff=frappe.get_doc("Warehouse",self.dropoff_station)
				if dropoff.station_code:
					self.destination_code=dropoff.station_code

	def before_submit(self):
		print(frappe.session.user)
		print(self.owner)
		self.user=self.user
		self.created_user=self.owner
		# self.save(ignore_permissions=True)
		if self.docstatus == 0:
			sales_invoice = frappe.get_doc("Sales Invoice", self.sales_invoice)
			attach_pdf(sales_invoice, self)

	def on_cancel(self):
		# frappe.throw("rrrrrrrrrrrrr")
		if self.consignment_id:
			fetch_sal_ord=frappe.get_doc("Sales Order",self.consignment_id)
			fetch_sal_ord.cancel()
		if self.sales_invoice:
			fetch_sal_inv=frappe.get_doc("Sales Invoice",self.sales_invoice)
			# fetch_sal_inv.grand_total=0
			# fetch_sal_inv.total=0
			# self.sales_invoice=""
			# frappe.db.commit()
			
			fetch_sal_inv.cancel()
			
			frappe.msgprint("Consignment Cancelled")
		# print(fetch_sal_ord,"999999999999999999999999999999999")


# ------------------ APIs ------------------ #

@frappe.whitelist(allow_guest=True)
def fetch_warehouse(user):
	# if frappe.session.user!='Administrator':
	user1=frappe.get_doc("User",user)
	print(user1)
	if frappe.db.exists("User Warehouse",{"user":user1.name}):
		userper=frappe.get_doc("User Warehouse",{"user":user1.name})
		warehouse=userper.warehouse
		return warehouse
	else:
		return False
	# else:
	# 	return False
@frappe.whitelist(allow_guest=True)
def fetch_customer_data( mobile_number):
	if frappe.db.exists("Customer", { "mobile_number": mobile_number}):
		customer = frappe.get_doc("Customer", {"mobile_number": mobile_number})
		return customer.as_dict()
@frappe.whitelist(allow_guest=True)
def fetch_receiver_data( mobile_number):
	if frappe.db.exists("Customer", { "mobile_number": mobile_number}):
		customer = frappe.get_doc("Customer", {"mobile_number": mobile_number})
		return customer.as_dict()
	else:
		pass
import requests
@frappe.whitelist()
def send_otp(receiver_number, otp,val):
	apikey = 'NmM2YjZmNzQzNDc1NmU0YjZlMzg0MzU0NGM0NzU4NTY='
	sender = 'COFNET'
	# message = f'Hi, your OTP code is: {otp} for KSRTC Registration. -COFBA NETWORKS'
	message = f'OTP for {receiver_number}  is {otp} and valid till {val} minutes.Do not share this OTP with anyone for security reasons.'
	
	# Make API request to send OTP
	response = requests.get('https://api.textlocal.in/send/', params={
		'apikey': apikey,
		'numbers': receiver_number,
		'message': message,
		'sender': sender,
		'otp': 'true'
	})
	
	# Process the response
	if response.status_code == 200:
		return response.text
	else:
		return None


				
						
						

@frappe.whitelist()
def fetch_item(weight, distance,box,pickup_station,dropoff_station):
	print(weight, distance,type(box),pickup_station,dropoff_station,"weight and distance")
	
	
	items = frappe.get_all("Item",{"disabled":0})
	
	for item_data in items:
		data={}
		itm=frappe.get_doc("Item",item_data.name)
		
		if itm.min_weight is not None and itm.max_weight is not None:
			# Item price calculation
			if float(weight) > 1 and float(distance)<=800:	
					if float(itm.min_weight) >1:
						if itm.min_distance is not None and itm.maxm_distance is not None:
							if float(itm.min_distance) <= float(distance) <= float(itm.maxm_distance):
									data["item"]=itm.name
									if itm.max_weight:
										data["mweight"]=float(itm.max_weight)
									else:
										data["mweight"]=0
					
									if itm.maxm_distance:
										data["mdis"]=float(itm.maxm_distance)
									else:
										data["mdis"]=0
									if itm.distance_rate:
										data["drate"]=itm.distance_rate
									else:
										data["drate"]=0
									if itm.weight_rate:
										data["rate"]=itm.weight_rate
									else:
										data["rate"]=0

									print(data,"data")
									
									return data
				

					
				
			if float(weight) > 1 and float(distance)>800:
					# frappe.throw("ge")
					if float(itm.min_weight) >1:
					# if float(itm.min_weight) <= float(weight) and float(itm.max_weight) == 0:
						# if itm.min_distance is not None and itm.maxm_distance is not None:
						# if float(itm.min_distance) <= float(distance) <= float(itm.maxm_distance):
						data["item"]=itm.name
						if itm.max_weight:
							data["mweight"]=float(itm.max_weight)
						else:
							data["mweight"]=0
							
						if itm.maxm_distance:
							data["mdis"]=float(itm.maxm_distance)
						else:
							data["mdis"]=0
						if itm.distance_rate:
							data["drate"]=itm.distance_rate
						else:
							data["drate"]=0
						if itm.weight_rate:
							data["rate"]=itm.weight_rate
						else:
							data["rate"]=0
						print(data,"data")

						return data
			
			if float(weight)<=1:
				if int(box)==1:
					if itm.min_distance is not None and itm.maxm_distance is not None:
						if float(itm.min_distance) <= float(distance) <= float(itm.maxm_distance):
							print(distance,"lllll",itm.min_distance,itm.maxm_distance)
							if float(itm.min_weight)==0.50001 and float(itm.max_weight)==1:
								print(itm.min_weight,itm.max_weight,"weight")
								data["item"]=itm.name
								# frappe.throw("hello")
							
								data["weight"]=itm.max_weight
								if itm.distance_rate:
									data["drate"]=itm.distance_rate
								else:
									data["drate"]=0
								# cal=frappe.get_doc("Warehouse",pickup_station)
								# print(pickup_station,"pickup_station")
								cal = frappe.get_doc('Warehouse',pickup_station)
								# print(cal.warehouse_type,"cal")
								if cal.warehouse_type=="Interstate Station":
									data["val"]=1
								else:
									data["val"]=0
								kal=frappe.get_doc("Warehouse",dropoff_station)
								if kal.warehouse_type=="Interstate Station":
									data["kal"]=1
								else:
									data["kal"]=0
							
								data["rate"]=itm.weight_rate
								# print("tttttttttttttttttttttttttttttttttttt")
								# print(data,"yyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
								return data			
				else:
					# frappe.throw("hai")
					if float(itm.min_weight) <= float(weight) <= float(itm.max_weight):			
						if itm.min_distance is not None and itm.maxm_distance is not None:
								if float(itm.min_distance) <= float(distance) <= float(itm.maxm_distance):
									print(box,"box")
									data["item"]=itm.name
									if itm.weight_rate:
										data["rate"]=itm.weight_rate
									else:
										data["rate"]=0
									cal = frappe.get_doc('Warehouse',pickup_station)
									print(cal.warehouse_type,"cal")
									if cal.warehouse_type=="Interstate Station":
										
										data["val"]=1
										# print(cal.warehouse_type,"hhhhhhhhhh")
										# print(data["val"],"hhhhhhhhhhhhhhhhh")
									else:
										print(cal.warehouse_type,"hhhhhhhhhh")
										data["val"]=0
										# frappe.throw("hello")
										# print(data["val"],"gggggggggggggggggggggg")
									kal=frappe.get_doc("Warehouse",dropoff_station)
									if kal.warehouse_type=="Interstate Station":
										data["kal"]=1
									else:
										data["kal"]=0
										
									if itm.distance_rate:
										data["drate"]=itm.distance_rate
									else:
										data["drate"]=0
									print(data,"data")	
									return data
			
					
@frappe.whitelist()
def cancel_booking(consignment_id, consignment_number):
	print("this is cancel booking")
	# frappe.throe("hello")
	if consignment_id != "":
		fetch_sal_ord=frappe.get_doc("Sales Order",consignment_id)
		fetch_sal_ord.consignment_number=""
		# fetch_sal_ord.db_update()
	consignment=frappe.get_doc("Consignment Booking",consignment_number)
	payment_list = frappe.get_all("Payment Entry",fields=["*"], filters={"party": consignment.full_name})
	print(payment_list,"payment_list")
	for payment in payment_list:
		payment_entry = frappe.get_doc("Payment Entry", payment["name"])
		for i in payment_entry.references:
			if i.reference_name==consignment.sales_invoice:
				# payment_entry = frappe.get_doc("Payment Entry", payment.name)
				payment_entry.cancel()
	consignment.cstatus="Cancelled"
	consignment.cancel()
@frappe.whitelist()	
def createlot(pickup_station,destination_station,bag_number,consignments,date1,vehicle,conductor,driver,on_Transit):
	print(pickup_station,destination_station,bag_number,on_Transit)
	print(type(on_Transit))
	print(type(consignments),"consignments")
	# print(values,"values")
	# print(type(values),"type")
	# valuelist=values.split(",")
	# keys = ["destination_station","pickup_station","bag_number"]

	# # Convert list to dictionary using zip
	# my_dict = dict(zip(keys, valuelist))

	# print(my_dict)
	if bag_number=="0":
	# frappe.throw("Please Enter Bag Number")
	# pass
		for i in range(0,1000):
			
			random_number = random.randint(100,99999)
			print(random_number,"random number")
			
			if not frappe.db.exists("Bag Number",{"number": random_number}):
				bag = frappe.new_doc("Bag Number")
				bag.number = random_number
				# bag.insert(ignore_permissions=True)
				bag.save(ignore_permissions=True)
				print(f"Generated and saved Bag Number: {random_number}")
				break
		# 	print(random_number)
		# print(bag,"gggggggggggggggggggggggggggggggggggggggggggg")
		# frappe.throw("Please Enter Bag Number")
	# def generate_unique_bag_number():

	# 	random_number = random.randint(10000, 99999)
	# 	if not frappe.db.exists("Bag Number", {"number": random_number}):
	# 		bag = frappe.new_doc("Bag Number")
	# 		bag.number = random_number
	# 		bag.status="Vacant"
	# 		bag.save(ignore_permissions=True)
	# 		print(f"Generated and saved Bag Number: {random_number}")
	# 		return random_number
	# if bag_number == "0":
	# 	unique_bag_number = generate_unique_bag_number()
	# 	print(f"Unique Bag Number: {unique_bag_number}")
	# 	# frappe.throw("bag number")
	# else:
	# 	# Handle other cases if needed
	# 	pass
		
	print(consignments,"consignments")
	lst = consignments.strip('[]').replace('"', '').split(',')

	print(lst)
	print(type(lst))
	lot=frappe.new_doc("LOT Number")
	
	lot.pickup_station=pickup_station
	lot.end_station=destination_station
	lot.bag_number=bag.number
	lot.posting_date=date1
	for i in lst:
		consin=frappe.get_doc("Consignment Booking",i)
		print(consin,"consin")
		if consin.full_name:
			cust=frappe.get_doc("Customer",consin.full_name)
			if cust.customer_primary_address:
				add=cust.customer_primary_address
				lot.append("destinations",{"consignment_number":i,"customer":consin.full_name,"delivery_note":consin.consignment_id,"address":add})

	lot.save(ignore_permissions=True)
	lot.submit()
	veh_assign=frappe.new_doc("Vehicle Assignment")
	veh_assign.start_point=pickup_station
	veh_assign.end_point=destination_station
	veh_assign.vehicle_=vehicle
	veh_det=frappe.get_doc("Vehicle",vehicle)
	veh_assign.rt_number=veh_det.rtc_number
	if veh_det.depot_name:
		veh_assign.make_=veh_det.depot_name
	if veh_det.engine_number:
		veh_assign.model=veh_det.engine_number
	veh_assign.condctor=conductor
	conduct_det=frappe.get_doc("Conductor",conductor)
	veh_assign.conductor_name=conduct_det.full_name
	veh_assign.conductor_phone_number=conduct_det.cell_number
	veh_assign.driver=driver
	driv_det=frappe.get_doc("Driver",driver)
	veh_assign.driver_name=driv_det.full_name
	veh_assign.driver_phone_number=driv_det.cell_number
	veh_assign.append("delivery_details",{"bag_number":bag.number,"order_transfer_lot":lot.name,"pickup_station":lot.pickup_station,"destination_station":lot.end_station})
	veh_assign.save(ignore_permissions=True)
	veh_assign.submit()
	if on_Transit =="1":
		veh=frappe.get_doc("Vehicle Assignment",veh_assign.name)
		mat=frappe.new_doc("Stock Entry")
		mat.purpose="Material Issue"
		mat.stock_entry_type="Material Issue"
		mat.vehicle_assignment=veh_assign.name
		
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
	else:
		pass
	# com=frappe.get_doc("Company",lot.company)
	# create_stock_entry()
	# "doc": frm.doc.name,
	# "company":frm.doc.company,
	# "posting_date":frm.doc.date,
	# "posting_time":frm.doc.time,
	# "purpose":"Material Issue",
	# "vehicle_assignment_id":frm.doc.name
	frappe.msgprint('LOT Number ' f'<a href="/app/lot-number/{lot.name}" target="blank">{lot.name} </a> Created Successfully ')
	frappe.msgprint('Vehicle Assignment ' f'<a href="/app/vehicle-assignment/{veh_assign.name}" target="blank">{veh_assign.name} </a> Created Successfully ')	
	# return 
	
@frappe.whitelist()
def check_lotID(**kwagrs):
	hasLotID = False
	conWithLot = []
	del kwagrs["cmd"]
	if frappe.session.user!='Administrator':
		get_warehouse=frappe.get_doc("User Warehouse",{"user":frappe.session.user})
		user_warehouse=get_warehouse.warehouse
	
		for key in kwagrs:
			consignment = frappe.get_doc("Consignment Booking", kwagrs[key])
			if consignment.lot_id:
				hasLotID = True
				conWithLot.append(consignment.name)
		return {
			"hasLot": hasLotID,
			"consignmentList": conWithLot,
			"user_warehouse":user_warehouse
		}
	else:
		for key in kwagrs:
			consignment = frappe.get_doc("Consignment Booking", kwagrs[key])
			if consignment.lot_id:
				hasLotID = True
				conWithLot.append(consignment.name)
		return {
			"hasLot": hasLotID,
			"consignmentList": conWithLot,
			"user_warehouse":""
		}
@frappe.whitelist()
def check_status(**kwagrs):
	hasLotID = False
	status = []
	del kwagrs["cmd"]
	if frappe.session.user!='Administrator':
		get_warehouse=frappe.get_doc("User Warehouse",{"user":frappe.session.user})
		user_warehouse=get_warehouse.warehouse
		for key in kwagrs:
			consignment = frappe.get_doc("Consignment Booking", kwagrs[key])
			if consignment.cstatus!="On Transit":
				hasLotID = True
				status.append(consignment.name)
				break
		return {
			"hasLot": hasLotID,
			"consignmentList": status,
			"user_warehouse":user_warehouse
		}
	else:
		for key in kwagrs:
			consignment = frappe.get_doc("Consignment Booking", kwagrs[key])
			if consignment.cstatus!="On Transit":
				hasLotID = True
				status.append(consignment.name)
				break
		return {
			"hasLot": hasLotID,
			"consignmentList": status,
			"user_warehouse":""
		}
	
@frappe.whitelist()	
def create_delivery_receipt(destination_station,bag_number,consignments,lot_number):
	print(destination_station,bag_number,consignments,lot_number,"1222222222")
	# frappe.throw("hello")
	lst = consignments.strip('[]').replace('"', '').split(',')
	delivery_receipt=frappe.new_doc("Delivery Trip Receipt")
	delivery_receipt.lot_destination=destination_station
	delivery_receipt.bag_number=bag_number
	delivery_receipt.consignment_number=lot_number
	delivery_receipt.delivery_date=frappe.utils.nowdate()
	delivery_receipt.dropoff_station=destination_station
	# delivery_receipt.
	print(delivery_receipt.bag_number,"delivery_receipt.bag_number")
	print(delivery_receipt.consignment_number,"delivery_receipt consignment_number")
	print(delivery_receipt.lot_destination,"delivery_receipt lot destination")
	for i in lst:
		consin=frappe.get_doc("Consignment Booking",i)
		print(consin,"consin")
		delivery_receipt.append("consignment_list",{"consignment":consin.name,"customer_name":consin.full_name,"customer_phone_number":consin.mobile_number,"receiver_name":consin.name1,"receiver_phone_number":consin.phone_number})
	delivery_receipt.save(ignore_permissions=True)
	delivery_receipt.submit()
	# for i in delivery_receipt.delivery_details:
	# 	veh_ass=frappe.get_doc()

	frappe.msgprint('Delivery Receipt ' f'<a href="/app/delivery-trip-receipt/{delivery_receipt.name}" target="blank">{delivery_receipt.name} </a> Created Successfully ')
