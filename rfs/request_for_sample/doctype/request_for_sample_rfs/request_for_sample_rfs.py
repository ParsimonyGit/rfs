# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class RequestForSampleRFS(Document):
	# pass
	def onload(self):
		info = self.get_status_dates()
		for i in info:
			print('-')
			print(i)
			prev=None
			for k,v in i.items():
				if v!=None:
					print(k,v)

					if prev:
						print(prev,'22')
						if prev < get_datetime(v):
							print(prev,get_datetime(v),prev < get_datetime(v) )
					prev=get_datetime(v)
					print('ww',prev)
		# self.set_onload('label_requirements', info)

	# def get_label_requirements(self):
	# 	# info={}
	# 	info={self.create_label}
	# 	# for row in self.get("sample_details") or []:
	# 	# 	if row.get("parameter") in ('Construction : Core Material & Structure','Gloss Level','Species','Color','Dimensions US customary units (metric)','Surface Treatment','Finish and Gloss Level'):
	# 	# 		info[row.get("parameter")] = row.get("value")
	# 	# print('info',info)
	# 	return info

	def get_status_dates(self):
		return frappe.db.sql(
		"""SELECT
	creation as `Open`,
	rfs_emailed_date as `RFS Emailed`,
	rfs_to_vendor_date as `RFS To Vendor`,
	rfs_from_vendor_date as `RFS From Vendor:`,
	rfs_received_date as `RFS Received`,
	rfs_in_review_date as `RFS In Review`,
	rfs_approved_date as `RFS Approved`,
	rfs_rejected_date as `RFS Rejected`,
	rfs_canceled_date as `RFS Canceled`
FROM
	`tabRequest For Sample RFS`
where name=%s""",
		self.name,
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