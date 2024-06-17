import frappe

def create_connections():
    update_dashboard_link_for_core_doctype(
        "Project", "Request For Sample RFS", "project", "Sourcing"
    )
    update_dashboard_link_for_core_doctype(
        "Project", "Sourcing SR", "project", "Sourcing"
    )    

def update_dashboard_link_for_core_doctype(
    doctype, link_doctype, link_fieldname, group=None
):
    try:
        d = frappe.get_doc("Customize Form")
        if doctype:
            d.doc_type = doctype
        d.run_method("fetch_to_customize")
        for link in d.get("links"):
            if (
                link.link_doctype == link_doctype
                and link.link_fieldname == link_fieldname
            ):
                # found so just return
                return
        d.append(
            "links",
            dict(
                link_doctype=link_doctype,
                link_fieldname=link_fieldname,
                table_fieldname=None,
                group=group,
            ),
        )
        d.run_method("save_customization")
        frappe.clear_cache()
    except Exception:
        frappe.log_error(frappe.get_traceback())