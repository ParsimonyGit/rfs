import frappe
from frappe import _

def execute():
	if frappe.db.exists("Email Template","Sourcing"):
		default_sourcing_email_template = frappe.db.get_value('Sourcing Settings SR', 'Sourcing Settings SR', 'default_sourcing_email_template')
		print('default_sourcing_email_template')
		if default_sourcing_email_template=='Sourcing':
			frappe.db.set_value('Sourcing Settings SR', 'Sourcing Settings SR', 'default_sourcing_email_template', None)
		frappe.db.sql(
			"""update `tabSourcing SR` set initial_email_template=NULL where initial_email_template='Sourcing'
		"""
		) 		
		print('here')
		frappe.db.sql("""Delete from `tabEmail Template` where name='Sourcing'""")
		frappe.db.commit()
