import frappe
from frappe import _

def get_context(context):
    if frappe.form_dict:
        context.rfs_name=frappe.form_dict.rfs_name
    carrier_list=frappe.db.get_all('Carrier RFS', pluck='name')      
    context.query_options=carrier_list
    return context

@frappe.whitelist(allow_guest=True)
def send_carrier_details(rfs_name, shipment_sample_carrier_name, shipment_sample_tracking_no,sample_from_vendor_remark=None):
        rfs_exist=frappe.db.exists('Request For Sample RFS', rfs_name)
        if rfs_exist==None:
            frappe.response[
                "message"
            ] = "Sorry: RFS doesn't exist in our system. Please take a screenshot and email us."
            return             
        frappe.db.set_value('Request For Sample RFS', rfs_name, {
            'shipment_sample_carrier_name': shipment_sample_carrier_name,
            'shipment_sample_tracking_no': shipment_sample_tracking_no,
            'sample_from_vendor_remark':sample_from_vendor_remark,
            'rfs_from_vendor_date':frappe.utils.now_datetime(),
            'status':'RFS From Vendor'
        })    
        return "okay"