# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt
#  sourcing request

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make
from frappe.utils.user import get_user_fullname,parse_addr
from frappe import _

STANDARD_USERS = ("Guest", "Administrator")

class SourcingSR(Document):
	def onload(self):
		info = self.get_initial_supplier_statistics()
		self.set_onload('initial_supplier_statistics', info)	

	def get_initial_supplier_statistics(self):
		data={}
		avg_star_rating=frappe.db.sql("""SELECT SUM(initial_supplier_rating)/COUNT(name)  as avg_star_rating 
		FROM `tabInitial Supplier Detail` where initial_sent=1 and parent='{sourcing_name}'"""
		.format(sourcing_name=self.name),as_dict=True,debug=0)[0]

		response_received_per=frappe.db.sql("""SELECT SUM(initial_received)/SUM(initial_sent) as response_received_per
		FROM `tabInitial Supplier Detail` where initial_sent=1 and parent='{sourcing_name}'"""
		.format(sourcing_name=self.name),as_dict=True,debug=0)[0]

		avg_response_time=frappe.db.sql("""SELECT IFNULL(((TIMESTAMPDIFF(DAY,initial_supplier_email_sent_date,initial_supplier_email_received_date))/COUNT(name)),0) as avg_response_time
		FROM `tabInitial Supplier Detail` where initial_supplier_email_received_date is not null and initial_supplier_email_sent_date is not null and parent='{sourcing_name}'"""
		.format(sourcing_name=self.name),as_dict=True,debug=0)[0]

		data.update(avg_star_rating)
		data.update(response_received_per)
		data.update(avg_response_time)
		return data

	def validate_email_id(self, args):
		if not args.initial_supplier_email:
			frappe.throw(
				_("Row {0}: For Supplier {1}, Email Address is Required to send an email").format(
					args.idx, frappe.bold(args.initial_supplier_name)
				)
			)

	@frappe.whitelist()
	def get_supplier_email_preview(self, initial_supplier_name):
		"""Returns formatted email preview as string."""
		initial_suppliers = list(filter(lambda row: row.initial_supplier_name == initial_supplier_name, self.initial_supplier_details))
		initial_supplier = initial_suppliers[0]
		message = self.supplier_initial_mail(data=initial_supplier,preview=True)
		return message

	@frappe.whitelist()
	def send_mail_to_initial_supplier(self):
		for initial_supplier in self.initial_supplier_details:
			if initial_supplier.initial_supplier_email is not None and initial_supplier.initial_sent==0:
				self.validate_email_id(initial_supplier)

		for initial_supplier in self.initial_supplier_details:
			if initial_supplier.initial_supplier_email is not None and initial_supplier.initial_sent==0:
				self.supplier_initial_mail(data=initial_supplier,preview=False)

	def supplier_initial_mail(self,data,preview=False):
		full_name = get_user_fullname(frappe.session["user"])
		if full_name == "Guest":
			full_name = "Administrator"

		doc_args = self.as_dict()
		doc_args.update({"initial_supplier": data.get("initial_supplier_name"),"user_fullname": full_name})

		subject = self.initial_email_subject or _("Product Inquiry")
		sender = frappe.session.user not in STANDARD_USERS and frappe.session.user or None
		message = frappe.render_template(self.initial_email_body, doc_args)

		if preview:
			return message

		attachments=None
		# attachments = self.get_attachments()
		# sender_full_name=self.get_sender_full_name(sender)
		default_sourcing_email_account = frappe.db.get_single_value("Sourcing Settings SR", "default_sourcing_email_account")
		if not default_sourcing_email_account:
			frappe.throw(
				_("Please set Default Sourcing Email Account in Sourcing Settings")
			)
		email_id = frappe.db.get_value('Email Account', default_sourcing_email_account, 'email_id')	
		self.send_email(data=data, sender=email_id,sender_full_name=full_name, subject=subject, message=message, attachments=attachments)

	def get_sender_full_name(self,sender):
		sender_name, sender_email = parse_addr(sender)
		sender_full_name=None
		if sender_full_name:
			self.sender_full_name = frappe.db.get_value("User", sender, "full_name")

		if self.sender_full_name:
			first_name, last_name = frappe.db.get_value(
				"Contact", filters={"email_id": sender_email}, fieldname=["first_name", "last_name"]
			) or [None, None]
			sender_full_name = (first_name or "") + (last_name or "")

		if self.sender_full_name:
			self.sender_full_name = sender_email
		return sender_full_name

	def get_attachments(self):
		attach_product_pdf_in_sourcing_email = frappe.db.get_single_value("Sourcing Settings SR", "attach_product_pdf_in_sourcing_email")
		default_sourcing_pdf_to_attach=frappe.db.get_single_value("Sourcing Settings SR", "default_sourcing_pdf_to_attach")
		print('-'*10)
		print(attach_product_pdf_in_sourcing_email,default_sourcing_pdf_to_attach)
		if attach_product_pdf_in_sourcing_email==0:
			return []
		attachments = frappe.attach_print(
			"Sourcing Settings SR",
			self.name,
			file_name="Product Details",
			print_format=default_sourcing_pdf_to_attach,
		)

		return [attachments]

	def send_email(self, data, sender, sender_full_name, subject, message, attachments):
		attach_product_pdf_in_sourcing_email = frappe.db.get_single_value("Sourcing Settings SR", "attach_product_pdf_in_sourcing_email")
		if attach_product_pdf_in_sourcing_email==0:
			print_format_attachment=None
		else:
			print_format_attachment=frappe.db.get_single_value("Sourcing Settings SR", "default_sourcing_pdf_to_attach") or None

		make(
			subject=subject,
			content=message,
			recipients=data.initial_supplier_email,
			sender=sender,
			sender_full_name=sender_full_name,
			attachments=attachments,
			print_format=print_format_attachment,
			send_email=True,
			doctype=self.doctype,
			name=self.name,
		)["name"]

		frappe.msgprint(_("Email Sent to Supplier {0}").format(data.initial_supplier_name))	

@frappe.whitelist()
def get_specification_template_details(specification_template_name):
	if not specification_template_name:
		return
	sample_template = frappe.get_doc('Sample Template RFS', specification_template_name)
	sample_template_details = []
	for i, parameter_row in enumerate(sample_template.get("template_parameters")):
		sample_template_details.append({'parameter':parameter_row.get('parameter'),'value':parameter_row.get('value')})
	return sample_template_details
