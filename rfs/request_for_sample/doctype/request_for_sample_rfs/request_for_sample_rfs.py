# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RequestForSampleRFS(Document):
	pass
	# def onload(self):
	# 	info = self.get_label_requirements()
	# 	self.set_onload('label_requirements', info)

	# def get_label_requirements(self):
	# 	# info={}
	# 	info={self.create_label}
	# 	# for row in self.get("sample_details") or []:
	# 	# 	if row.get("parameter") in ('Construction : Core Material & Structure','Gloss Level','Species','Color','Dimensions US customary units (metric)','Surface Treatment','Finish and Gloss Level'):
	# 	# 		info[row.get("parameter")] = row.get("value")
	# 	# print('info',info)
	# 	return info

@frappe.whitelist()
def get_sample_template_details(sample_template_name):
	if not sample_template_name:
		return
	sample_template = frappe.get_doc('Sample Template RFS', sample_template_name)
	sample_template_details = []
	for i, parameter_row in enumerate(sample_template.get("template_parameters")):
		sample_template_details.append({'parameter':parameter_row.get('parameter'),'value':parameter_row.get('value')})
	return sample_template_details