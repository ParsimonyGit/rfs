import pyqrcode
from frappe.utils import get_url_to_form

def get_qr_code(doctype,docname,scale=5):
    qr_text=get_url_to_form(doctype,docname)
    return pyqrcode.create(qr_text).png_as_base64_str(scale=scale, quiet_zone=1)