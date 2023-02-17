import frappe


def after_insert_communication(doc, method=None):
    """on email sent from RFS change status"""
    try:
        reference_doctype = doc.get("reference_doctype")
        reference_name = doc.get("reference_name")
        creation=doc.get("creation")
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
    except Exception:
        frappe.log_error(frappe.get_traceback())