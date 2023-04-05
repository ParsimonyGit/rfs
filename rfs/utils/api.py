import frappe


def after_insert_communication(doc, method=None):
    """on email sent from RFS change status"""
    try:
        reference_doctype = doc.get("reference_doctype")
        reference_name = doc.get("reference_name")
        creation=doc.get("creation")

        #  On RFS email sent
        if (
            doc.communication_type == "Communication"
            and doc.sent_or_received == "Sent"
            and reference_doctype
            and reference_name
        ):
            if reference_doctype == "Request For Sample RFS":
                frappe.db.set_value(
                    reference_doctype, reference_name, "status", "RFS Emailed"
                )
                frappe.db.set_value(
                    reference_doctype,
                    reference_name,
                    "rfs_emailed_date",
                    creation
                )
                frappe.reload_doc("request_for_sample", "doctype", "request_for_sample_rfs")


        #  On Sourcing initial email sent
            if reference_doctype == "Sourcing SR":
                sourcing_initial_email_subject= frappe.db.get_value('Sourcing SR', reference_name, 'initial_email_subject')
                if sourcing_initial_email_subject and doc.subject==sourcing_initial_email_subject:
                    initial_supplier_detail_name=frappe.db.get_all('Initial Supplier Detail', 
                                                                    fields=['name'],
                                                                    filters={'parent': ['=', reference_name],'initial_supplier_email': ['=', doc.recipients] })                    
                    if len(initial_supplier_detail_name)>0:
                        supplier_detail_name=initial_supplier_detail_name[0].name
                        frappe.db.set_value(
                            'Initial Supplier Detail',
                            supplier_detail_name,
                            "initial_sent",
                            1
                        )
                        frappe.db.set_value(
                            'Initial Supplier Detail',
                            supplier_detail_name,
                            "initial_supplier_email_sent_date",
                            creation
                        )                        
                        frappe.db.set_value(
                            'Initial Supplier Detail',
                            supplier_detail_name,
                            "initial_sent_communication_name",
                            doc.name
                        )                    
                        frappe.reload_doc("request_for_sample", "doctype", "sourcing_sr")

        #  On Sourcing initial email received
        if (
            doc.communication_type == "Communication"
            and doc.sent_or_received == "Received"
            and reference_doctype
            and reference_name
        ):        
            if reference_doctype == "Sourcing SR":
                if doc.in_reply_to:
                    initial_supplier_detail_name=frappe.db.get_all('Initial Supplier Detail', 
                                                                    fields=['name'],
                                                                    filters={'parent': ['=', reference_name],'initial_sent_communication_name': ['=', doc.in_reply_to] })                    
                    if len(initial_supplier_detail_name)>0:
                        supplier_detail_name=initial_supplier_detail_name[0].name
                        frappe.db.set_value(
                            'Initial Supplier Detail',
                            supplier_detail_name,
                            "initial_received",
                            1
                        )
                        frappe.db.set_value(
                            'Initial Supplier Detail',
                            supplier_detail_name,
                            "initial_supplier_email_received_date",
                            creation
                        )                        
                        frappe.db.set_value(
                            'Initial Supplier Detail',
                            supplier_detail_name,
                            "initial_received_communication_name",
                            doc.name
                        )                    
                        frappe.reload_doc("request_for_sample", "doctype", "sourcing_sr")


    except Exception:
        frappe.log_error(frappe.get_traceback())