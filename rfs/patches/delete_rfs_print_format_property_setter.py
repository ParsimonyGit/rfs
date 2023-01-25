import frappe


def execute():
	frappe.reload_doctype("Request For Sample RFS")
	property_setter_name = frappe.db.exists(
		"Property Setter", 
		dict(doc_type="Request For Sample RFS", property="default_print_format",value="Sample Request Form")
	)
	if property_setter_name:    
		frappe.db.sql(
			"""
			DELETE FROM `tabProperty Setter`
			WHERE `tabProperty Setter`.doc_type='Request For Sample RFS'
				AND `tabProperty Setter`.value='Sample Request Form'
				AND `tabProperty Setter`.property='default_print_format'
		"""
		)        