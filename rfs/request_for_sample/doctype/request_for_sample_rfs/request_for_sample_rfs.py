# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class RequestForSampleRFS(Document):
	# pass
	def onload(self):
		info = self.get_status_dates()
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


@frappe.whitelist()
def get_rfs_details(doctype, start, end, field_map, filters=None, fields=None):
	events = []
	event_color = {
			'Open':'#F0F8FE',
			'RFS Emailed':'#dafafa',
			'RFS To Vendor':'#FEEDF3',
			'RFS From Vendor':'#F2F2FD',
			'RFS Received':'#F0F8FE',
			'RFS In Review':'#FEF4E2',
			'RFS Approved':'#F4FAEE',
			'RFS Rejected':'#FFF5F5',
			'RFS Canceled':'#F9FAFA'	
		}

	from frappe.desk.reportview import get_filters_cond

	conditions = get_filters_cond("Request For Sample RFS", filters, [])
	rfs_details = frappe.db.sql(
		"""select t.name,t.project,t.supplier,t.status,t.from_time, max(t.to_time) as to_time from 
(
	select name,project,supplier,status,creation as from_time, creation as to_time, 'Open' as rfs_history_status, 'light blue' as rfs_status_color  from `tabRequest For Sample RFS` where 1=1 {0} union all 
	select name,project,supplier,status,creation as from_time, rfs_emailed_date as to_time, 'RFS Emailed' as rfs_history_status,'cyan' as rfs_status_color  from `tabRequest For Sample RFS` where 1=1 {0}  union all 
	select name,project,supplier,status,creation as from_time, rfs_to_vendor_date as to_time, 'RFS To Vendor' as rfs_history_status, 'pink' as rfs_status_color from `tabRequest For Sample RFS`  where 1=1 {0}  union all 
	select name,project,supplier,status,creation as from_time, rfs_from_vendor_date as to_time, 'RFS From Vendor' as rfs_history_status, 'purple' as rfs_status_color from `tabRequest For Sample RFS` where 1=1 {0}     union all 
	select name,project,supplier,status,creation as from_time, rfs_received_date as to_time, 'RFS Received' as rfs_history_status,  'blue' as rfs_status_color  from `tabRequest For Sample RFS`  where 1=1 {0} union all 
	select name,project,supplier,status,creation as from_time, rfs_in_review_date as to_time, 'RFS In Review' as rfs_history_status, 'yellow' as rfs_status_color  from `tabRequest For Sample RFS` where 1=1 {0}  union all 
	select name,project,supplier,status,creation as from_time, rfs_approved_date as to_time, 'RFS Approved' as rfs_history_status,  'green' as rfs_status_color from `tabRequest For Sample RFS`  where 1=1 {0} union all 
	select name,project,supplier,status,creation as from_time, rfs_rejected_date as to_time, 'RFS Rejected' as rfs_history_status, 'red' as rfs_status_color  from `tabRequest For Sample RFS`  where 1=1 {0} union all 
	select name,project,supplier,status,creation as from_time, rfs_canceled_date as to_time, 'RFS Canceled' as rfs_history_status,  'gray' as rfs_status_color from `tabRequest For Sample RFS`    where 1=1 {0}
) t
WHERE t.to_time is not null
group by t.name""".format(
			conditions
		),
		as_dict=1
	)

	for d in rfs_details:
		subject_data = []
		for field in ["name","project","supplier","status"]:
			if not d.get(field):
				continue

			subject_data.append(d.get(field))

		color = event_color.get(d.status)
		rfs_detail_data = {
			"from_time": d.from_time,
			"to_time": d.to_time,
			"name": d.name,
			"subject": "\n".join(subject_data),
			"color": color if color else "#89bcde",
		}

		events.append(rfs_detail_data)
	return events
