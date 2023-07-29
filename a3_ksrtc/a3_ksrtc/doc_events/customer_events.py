import frappe

def after_insert(doc, method):
	if not frappe.db.exists("Contact", {"first_name":doc.customer_name, "mobile_no":doc.mobile_number}):
		contact = frappe.new_doc("Contact")
		contact.first_name = doc.customer_name
		if doc.email:
			contact.append("email_ids", {
			"email_id": doc.email,
			"is_primary": 1,
		})
		contact.append("phone_nos", {
			"phone": doc.mobile_number,
			"is_primary_phone": 1,
			"is_primary_mobile_no": 1,
		})
		contact.append("links", {
			"link_doctype": "Customer",
			"link_name": doc.name,
			"link_title": doc.name,
		})
		
		contact.insert()
		if contact.name:
			doc.customer_primary_contact = contact.name
	# if doc.mobile_number and doc.email:
	# 	if not frappe.db.exists("User", {"first_name":doc.customer_name, "mobile_no":doc.mobile_number,"email":doc.email}):
			
	# 			user = frappe.get_doc(
	# 				{
	# 					"doctype": "User",
	# 					"mobile_no": doc.mobile_number,
	# 					"user.phone" : doc.mobile_number,
	# 					"first_name":doc.customer_name,

						
						
	# 					"email":doc.email,
	# 					"enabled": 1,	
	# 					"role_profile_name":"KSRTC Customer",
	# 					"user_type": "Website User",
	# 					"send_welcome_email":0
	# 				}
	# 			)
	# 			user.flags.ignore_permissions = True
	# 			user.flags.ignore_password_policy = True
	# 			user.insert()
	# 			frappe.msgprint('User ' f'<a href="/app/user/{user.name}" target="blank">{user.name} </a> Created Successfully ')
	# 	else:
	# 		frappe.throw("User exists with same mobile number")

	add=frappe.new_doc("Address")
	if doc.ad1:
		add.address_title=doc.ad1
	else:  
		add.address_title="NIL"
	if doc.ad2:
		add.address_line1=doc.ad2
	else:
		add.address_line1="NIL"
	if doc.ad3:
		add.city=doc.ad3
	else:
		add.city="NIL"
	
	if doc.pin:
		add.pincode=doc.pin
	else:
		add.pincode="NIL"
	if doc.state:
		add.state=doc.state
	if doc.tax_category:
		add.tax_category=doc.tax_category
	add.address_type="Shipping"
	add.append("links", {
		"link_doctype": "Customer",
		"link_name": doc.name,
		"link_title": doc.name,
	})
	add.insert()
		# doc.customer_address=add.name
	if add.name:
		doc.customer_primary_address=add.name
	if contact.name:
		doc.customer_primary_contact = contact.name
	doc.save()
		