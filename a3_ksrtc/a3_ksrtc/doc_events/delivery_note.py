import frappe

def on_submit(doc,methods):
    doc.status="Closed"
    doc.update_status(doc.status)
    
    if doc.delivery_trip_receipt:
        con=frappe.get_doc("Consignment Booking",doc.delivery_trip_receipt)
        con.cstatus="Delivered"
        if con.lot_id:
            lot=frappe.get_doc("LOT Number",con.lot_id)
            lot.transfer_status="Delivered"
            lot.save()
            lot.submit()
        if con.consignment_id:
            sal=frappe.get_doc("Sales Order",con.consignment_id)
            print(sal)
            sal.consignment_status="Delivered"
            sal.save()
            sal.submit()
        con.save()
        con.submit()
@frappe.whitelist(allow_guest=True)
def get_data_from_receipt(trip_receipt):
    data_from_receipt = []
    data = {}
    con=frappe.get_doc("Consignment Booking",trip_receipt)
    if con.dropoff_station:
            data["station"]=con.dropoff_station
    for shipment in con.shipment_details:
        
        
        data["type_of_shipmentitem"] = shipment.type_of_shipmentitem
        it=frappe.get_doc("Item",shipment.type_of_shipmentitem)
        data["description"]=it.description
        data["stock_uom"]=it.stock_uom
        data["quantity"] = shipment.quantity
        # data["rate"] = shipment.
        data["price"] = shipment.price
        data_from_receipt.append(data)
    return {"data": data_from_receipt}