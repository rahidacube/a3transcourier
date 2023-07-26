# # Copyright (c) 2023, Acube and contributors
# # For license information, please see license.txt

# import frappe
# from frappe import _
# from datetime import datetime
# import datetime as dt

# def execute(filters=None):
# 	filters = {'delivery_date': ['>=', datetime.now().date()], "docstatus":1}
# 	current_date = dt.date.today()
# 	count=[]

# # Get the first date of the current month
# 	first_date = current_date.replace(day=1)
# 	users=frappe.get_all("User",filters={"enabled":1,"user_type":"System User"})
# 	for user in users:
# 		data={}
# 		consignment_list = frappe.get_all("Consignment Booking", fields=["*"],filters={"user":user.name,"delivery_date":['>=', first_date],"docstatus":1},group_by="delivery_date")
# 		print(consignment_list)
# 		print(len(consignment_list),"Length")
# 		data["user"]=user.name
# 		data["count"]=len(consignment_list)
# 		# data["delivery_date"]=consignment_list[0].delivery_date


# 	# if frappe.session.user != "Administrator":
# 	# 	filters["user"] = frappe.session.user
# 	# consignment_list = frappe.get_all("Consignment Booking", fields=[ "user", "delivery_date", "pickup_station", "payment_method", "payment_status", "cost",], filters=filters)
# 	# print(consignment_list)
# 	columns= [
		
# 		{
# 			'fieldname': 'user',
# 			'label': _('User'),
# 			'fieldtype': 'Data'
# 		},
		
# 		{
# 			'fieldname': 'delivery_date',
# 			'label': _('Date'),
# 			'fieldtype': 'Date',
			
# 		},
# 		{
# 			'fieldname': 'count',
# 			'label': _('Total Consignmnets'),
# 			'fieldtype': 'Data'
# 		},
# 		{
# 			'fieldname': 'pickup_station',
# 			'label': _('Station'),
# 			'fieldtype': 'Link',
#    			'options': 'Warehouse'	   
# 		},
#   		{
# 			'fieldname': 'payment_method',
# 			'label': _('Payment Method'),
# 			'fieldtype': 'Select',  
# 		},
#   		{
# 			'fieldname': 'payment_status',
# 			'label': _('Payment Status'),
# 			'fieldtype': 'Select',  
# 		},
# 		{
# 			'fieldname': 'total;',
# 			'label': _('Total Amount'),
# 			'fieldtype': 'Currency',		   
# 		},

		
# 	]
# 	data=consignment_list
# 	report_summary = [{
# 		"value": len(consignment_list),
# 		"indicator": "Green",
# 		"label": _("Total Count"),
# 		"datatype": "Data",
# }]
# 	return columns, data, None, None, report_summary
