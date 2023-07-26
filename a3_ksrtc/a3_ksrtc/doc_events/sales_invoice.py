# import frappe

# def on_update(doc, methods):
#     if doc.pdf_doc:
#         getfile=frappe.get_doc("File",{"file_url":doc.pdf_doc})
#         res = getfile.name
#         print(res,"ghjklkjhgghjkkjhgghjkjhhjjhghjjhghjjhfk")
#         frappe.db.delete("File",res)
#         fallback_language = frappe.db.get_single_value("System Settings", "language") or "en"
#         args = {
#             "doctype": doc.doctype,
#             "name": doc.name,
#             "title": doc.get_title(),
#             "lang": getattr(doc, "language", fallback_language),
#             "show_progress": 0
#         }
#         fileurl = execute(**args)
#         url=frappe.utils.get_url()
#         doc.pdf_doc = fileurl
#         url=str(url)+str(doc.pdf_doc)
#         doc.attachment_url=url

#         attachments = frappe.get_all("File", filters={"attached_to_doctype":doc.doctype, "attached_to_name":doc.name}, fields=["name", "file_url"])
#         for attachment in attachments:
#             if attachment["file_url"] != fileurl:
#                 attach = get_doc("File", attachment["name"])
#                 attach.delete()