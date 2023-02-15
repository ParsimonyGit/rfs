# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class RequestForSampleRFS(Document):
	# pass
	def onload(self):
		info = self.get_status_dates()
		print(info)
		self.set_onload('status_history', info)	

	def get_status_dates(self):
		return frappe.db.sql(
		"""select t.status as status,DATE_FORMAT(t.creation_date,'%b %d %Y ,  %k:%i') as creation_date,color from 
(
	select creation as creation_date, 'Open' as status, 'light blue' as color  from `tabRequest For Sample RFS` where name='{rfs_name}' union all 
	select rfs_emailed_date, 'RFS Emailed' as status,'cyan' as color  from `tabRequest For Sample RFS`  where name='{rfs_name}' union all 
	select rfs_to_vendor_date, 'RFS To Vendor' as status, 'pink' as color from `tabRequest For Sample RFS`   where name='{rfs_name}' union all 
	select rfs_from_vendor_date, 'RFS From Vendor' as status, 'purple' as color from `tabRequest For Sample RFS`    where name='{rfs_name}' union all 
	select rfs_received_date, 'RFS Received' as status,  'blue' as color  from `tabRequest For Sample RFS` where name='{rfs_name}' union all 
	select rfs_in_review_date, 'RFS In Review' as status, 'yellow' as color  from `tabRequest For Sample RFS`  where name='{rfs_name}' union all 
	select rfs_approved_date, 'RFS Approved' as status,  'green' as color from `tabRequest For Sample RFS`  where name='{rfs_name}' union all 
	select rfs_rejected_date, 'RFS Rejected' as status, 'red' as color  from `tabRequest For Sample RFS`  where name='{rfs_name}' union all 
	select rfs_canceled_date, 'RFS Canceled' as status,  'gray' as color from `tabRequest For Sample RFS`   where name='{rfs_name}' 
) t
where t.creation_date is not null
order by t.creation_date ASC """.format(rfs_name=self.name),	
		as_dict=True,
	)

@frappe.whitelist()
def get_sample_template_details(sample_template_name):
	if not sample_template_name:
		return
	sample_template = frappe.get_doc('Sample Template RFS', sample_template_name)
	sample_template_details = []
	for i, parameter_row in enumerate(sample_template.get("template_parameters")):
		sample_template_details.append({'parameter':parameter_row.get('parameter'),'value':parameter_row.get('value')})
	return sample_template_details

@frappe.whitelist()
def get_supplier_address_html(address):
	address_display = ""
	if address:
		address_display = frappe.get_doc("Address", address).get_display()
	return address_display	