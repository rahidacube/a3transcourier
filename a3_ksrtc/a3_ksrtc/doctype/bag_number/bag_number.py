# Copyright (c) 2023, Acube and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BagNumber(Document):
	pass
# @frappe.whitelist()
	
	
# def fetch_stationcode(user):
# 	if frappe.db.exists("User Warehouse",{"user":user}):
# 		user_war=frappe.get_doc("User Warehouse",{"user":user})
# 		if user_war.warehouse:
# 			war=frappe.get_doc("Warehouse",user_war.warehouse)
# 			if war.station_code1:
# 				data= war.station_code1
# 				return data
	
