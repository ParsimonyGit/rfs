import frappe
from frappe import _

def get_context(context):
    if frappe.form_dict:
        context.rfs_name=frappe.form_dict.rfs_name
    carrier_list=frappe.db.get_all('Carrier RFS', pluck='name')      
    context.query_options=carrier_list
    return context

@frappe.whitelist(allow_guest=True)
def send_carrier_details(rfs_name, shipment_sample_carrier_name, shipment_sample_tracking_no):
        frappe.db.set_value('Request For Sample RFS', rfs_name, {
            'shipment_sample_carrier_name': shipment_sample_carrier_name,
            'shipment_sample_tracking_no': shipment_sample_tracking_no
        })    
