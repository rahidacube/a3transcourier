import frappe


@frappe.whitelist()
def get_data_from_receipt(trip_receipt):
    data_from_receipt = []
    receipt = frappe.get_doc("Delivery Trip Receipt", trip_receipt)
    
    for shipment in receipt.shipment_details:
        data = {}
        data["type_of_shipmentitem"] = shipment.type_of_shipmentitem
        data["weight"] = receipt.weight
        data["rate"] = shipment.rate
        data["price"] = shipment.price
        data_from_receipt.append(data)
    return {"data": data_from_receipt}
@frappe.whitelist(allow_guest=True)
def fetch_consignment(lot_number):
    lot = frappe.get_doc("LOT Number", lot_number)
    consignment_list = []

    for consignment in lot.destinations:
        data = {}

        consign = frappe.get_doc("Consignment Booking", consignment.consignment_number)
        data["consignment_id"] = consignment.consignment_number
        data["customer_name"] = consign.full_name
        data["customer_phone"] = consign.mobile_number
        data["receiver_name"] = consign.name1
        data["receiver_phone"] = consign.phone_number
        data["delivery_date"] = consign.delivery_date
        data["delivery_time"] = consign.delivery_time
        data["bag_number"] = lot.bag_number

        consignment_list.append(data)

    return consignment_list



@frappe.whitelist(allow_guest=True)
def fetch_lot(bag):
    print(bag)
    if frappe.db.exists("LOT Number", {"bag_number": bag,"transfer_status":"On-Transit"}):
        lot = frappe.get_doc("LOT Number", {"bag_number": bag,"transfer_status":"On-Transit"})
        data = {}
        data["name"]=lot.name
        return data
    else:
        return False    
