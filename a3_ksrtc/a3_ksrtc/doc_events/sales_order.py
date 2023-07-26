import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_order_transfer(source_name, target_doc=None):
    def update_stop_details(source_doc, target_doc, source_parent):
        consignment = frappe.get_doc("Consignment Booking", {"consignment_id": source_name})
        target_doc.customer = source_parent.customer
        target_doc.consignment_number = consignment.name
        target_doc.address = source_parent.shipping_address_name
        target_doc.customer_address = source_parent.shipping_address
        target_doc.contact = source_parent.contact_person
        target_doc.customer_contact = source_parent.contact_display
        target_doc.grand_total = source_parent.grand_total

        # Append unique Delivery Notes in Delivery Trip
        delivery_notes.append(target_doc.delivery_note)
        

    delivery_notes = []

    doclist = get_mapped_doc(
        "Sales Order",
        source_name,
        
        {
            "Sales Order": {"doctype": "LOT Number", "validation": {"docstatus": ["=", 1]}},
            "Sales Order Item": {
                "doctype": "Destination List",
                "field_map": {"parent": "delivery_note"},
                "condition": lambda item: item.parent not in delivery_notes,
                "postprocess": update_stop_details,
            },
        },
        target_doc,
    )

    return doclist
