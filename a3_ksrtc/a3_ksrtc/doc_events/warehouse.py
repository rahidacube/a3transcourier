
# import frappe

# import pyqrcode


# def after_insert(doc, method):
#     url = pyqrcode.create('doc.name')
#     print(url)
#     doc.qr_code_image=url.terminal(quiet_zone=1)
#     print(doc.qr_code_image,"hiulll")
#     doc.qr_preview=url.terminal(quiet_zone=1)
#     print(doc.qr_preview,"hiulll")
#     doc.save()
   
# from PIL import Image
# import qrcode
# import io
# import base64
# from frappe.utils.file_manager import save_file
# from frappe.utils import get_files_path

# def after_insert(doc, method):
#     qr_code = qrcode.make(doc.name)
#     image_stream = io.BytesIO()
#     qr_code.save(image_stream, format='PNG')
#     file_name = f'{doc.name}_qr_code.png'
#     file_path = get_files_path(file_name)
#     file_url = save_file(file_name, image_stream.getvalue(), doc.doctype, doc.name)
#     doc.qr_code_image = file_name
#     doc.qr_preview = f'<img src="{file_path}" alt="QR Code Preview">'
    

#     doc.save()

    
