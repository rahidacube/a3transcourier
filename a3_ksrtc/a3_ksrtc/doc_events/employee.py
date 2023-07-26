import frappe

@frappe.whitelist(allow_guest=True)
def get_warehouse(user):
    data={}
    userwarehouse = frappe.get_doc("User Warehouse", {"user": user})
    data['warehouse']=userwarehouse.warehouse
    return data