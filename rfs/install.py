import frappe

def create_files_for_logo():
    print("Creating files for logo...")
    
    ##### Check file is already exists or not #####
    app_logo_file_exists = frappe.db.exists("File", {"file_name": "parsimony_logo.png", "attached_to_doctype": "Website Settings", "attached_to_name": "Website Settings", "attached_to_field": "app_logo"})
    print("App logo file exists:-----------------", app_logo_file_exists)
    if app_logo_file_exists:
        pass
    else:
        app_logo_file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": "parsimony_logo.png",
            "is_private": 0,
            "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo.png"), "rb").read(),
            "attached_to_doctype": "Website Settings",
            "attached_to_name": "Website Settings",
            "attached_to_field": "app_logo"
        })
        app_logo_file_doc.insert(ignore_permissions=True)

    favicon_file_exists = frappe.db.exists("File", {"file_name": "parsimony_logo.png", "attached_to_doctype": "Website Settings", "attached_to_name": "Website Settings", "attached_to_field": "favicon"})
    print("Favicon file exists:-----------------", favicon_file_exists)
    if favicon_file_exists:
        pass
    else:
        favicon_file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": "parsimony_logo.png",
            "is_private": 0,
            "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo.png"), "rb").read(),
            "attached_to_doctype": "Website Settings",
            "attached_to_name": "Website Settings",
            "attached_to_field": "favicon"
        })
        favicon_file_doc.insert(ignore_permissions=True)

    splash_image_file_exists = frappe.db.exists("File", {"file_name": "parsimony_logo_with_name.png", "attached_to_doctype": "Website Settings", "attached_to_name": "Website Settings", "attached_to_field": "splash_image"})
    print("Splash image file exists:-----------------", splash_image_file_exists)
    if splash_image_file_exists:
        splash_image_file_url = frappe.get_value("File", splash_image_file_exists, "file_url")
    else:
        splash_image_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": "parsimony_logo_with_name.png",
            "is_private": 0,
            "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo_with_name.png"), "rb").read(),
            "attached_to_doctype": "Website Settings",
            "attached_to_name": "Website Settings",
            "attached_to_field": "splash_image"
        })
        splash_image_doc.insert(ignore_permissions=True)
        frappe.db.commit()  # Commit the transaction to ensure the file is saved
        splash_image_file_url = splash_image_doc.file_url
        print("Splash image file created successfully.", "File Name:", splash_image_doc.name, "File URL:", splash_image_doc.file_url)
    
    frappe.db.set_value("Website Settings", "Website Settings", "splash_image", splash_image_file_url)  # Update the splash_image field in Website Settings
    frappe.db.set_value("Website Settings", "Website Settings", "banner_image", splash_image_file_url)  # Update the banner_image field in Website Settings

    footer_image_file_exists = frappe.db.exists("File", {"file_name": "parsimony_logo.png", "attached_to_doctype": "Web Template", "attached_to_name": "Parsimony Footer"})
    if footer_image_file_exists:
        pass
    else:
        footer_image_file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": "parsimony_logo.png",
            "is_private": 0,
            "content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo.png"), "rb").read(),
            "attached_to_doctype": "Web Template",
            "attached_to_name": "Parsimony Footer"
        })
        footer_image_file_doc.insert(ignore_permissions=True)