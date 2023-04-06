import frappe
from frappe import _
from frappe.utils import cstr, cint

def get_context(context):
    if frappe.form_dict:
        context.rfs_name=frappe.form_dict.rfs_name
    carrier_list=frappe.db.get_all('Carrier RFS', pluck='name')      
    context.query_options=carrier_list
    return context

@frappe.whitelist(allow_guest=True)
def send_carrier_details(**args):
        args = args and frappe._dict(args) or frappe.form_dict
        rfs_name=args.rfs_name
        shipment_sample_carrier_name=args.shipment_sample_carrier_name
        shipment_sample_tracking_no=args.shipment_sample_tracking_no
        sample_from_vendor_remark=args.sample_from_vendor_remark or None         
        rfs_exist=frappe.db.exists('Request For Sample RFS', rfs_name)
        if rfs_exist==None:
            frappe.response[
                "message"
            ] = "Sorry: RFS doesn't exist in our system. Please take a screenshot and email us."
            return             
        # frappe.db.set_value('Request For Sample RFS', rfs_name, {
        #     'shipment_sample_carrier_name': shipment_sample_carrier_name,
        #     'shipment_sample_tracking_no': shipment_sample_tracking_no,
        #     'sample_from_vendor_remark':sample_from_vendor_remark,
        #     'rfs_from_vendor_date':frappe.utils.now_datetime(),
        #     'status':'RFS From Vendor'
        # })  
        rfs = frappe.get_doc('Request For Sample RFS', rfs_name)
        rfs.shipment_sample_carrier_name=shipment_sample_carrier_name
        rfs.shipment_sample_tracking_no=shipment_sample_tracking_no
        rfs.sample_from_vendor_remark=sample_from_vendor_remark
        rfs.rfs_from_vendor_date=frappe.utils.now_datetime()
        rfs.status='RFS From Vendor'
        files = frappe.request.files
        if "file" in files:
            is_private = frappe.form_dict.is_private or 0
            file_url = frappe.form_dict.file_url
            folder = frappe.form_dict.folder or "Home"
            method = frappe.form_dict.method
            content = None
            filename = None

            file = files["file"]
            content = file.stream.read()
            filename = file.filename

            frappe.local.uploaded_file = content
            frappe.local.uploaded_filename = filename

            try:
               
                ret = frappe.get_doc(
                    {
                        "doctype": "File",
                        "attached_to_doctype": rfs.doctype,
                        "attached_to_name":rfs.name ,
                        "folder": folder,
                        "file_name": filename,
                        "file_url": file_url,
                        "is_private": cint(is_private),
                        "content": content,
                    }
                )
                ret.save(ignore_permissions=True)
                rfs.append('factory_sample_pictures',{
                    'photo_id':filename,
                    'attach_sample_image':ret.file_url
                })      
                rfs.save(ignore_permissions=True)           
                # return doc, ret
            except frappe.DuplicateEntryError:
                # ignore pass
                ret = None
                frappe.db.rollback()             

        


        return "okay"