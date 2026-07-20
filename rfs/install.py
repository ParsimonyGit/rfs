import frappe

def before_install():
    """
    This function is called before the installation of the app.
    It can be used to perform any setup or configuration required before the app is installed.
    """
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "parsimony_logo.png",
        "is_private": 0,
        "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo.png"), "rb").read(),
        "attached_to_doctype": "Website Settings",
        "attached_to_name": "Website Settings",
        "attached_to_field": "app_logo"
    })
    file_doc.insert(ignore_permissions=True)

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "parsimony_logo.png",
        "is_private": 0,
        "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo.png"), "rb").read(),
        "attached_to_doctype": "Website Settings",
        "attached_to_name": "Website Settings",
        "attached_to_field": "favicon"
    })
    file_doc.insert(ignore_permissions=True)

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "parsimony-logo-gold_71293707.png",
        "is_private": 0,
        "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony-logo-gold_71293707.png"), "rb").read(),
        "attached_to_doctype": "Website Settings",
        "attached_to_name": "Website Settings",
        "attached_to_field": "splash_image"
    })
    file_doc.insert(ignore_permissions=True)

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "parsimony-logo-gold_71293707.png",
        "is_private": 0,
        "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony-logo-gold_71293707.png"), "rb").read(),
        "attached_to_doctype": "Website Settings",
        "attached_to_name": "Website Settings",
        "attached_to_field": "banner_image"
    })
    file_doc.insert(ignore_permissions=True)

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "parsimony_logo.png",
        "is_private": 0,
        "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo.png"), "rb").read(),
        "attached_to_doctype": "Web Template",
        "attached_to_name": "Parsimony Footer"
    })
    file_doc.insert(ignore_permissions=True)