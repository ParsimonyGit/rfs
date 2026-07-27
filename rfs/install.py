import frappe

def create_files_for_logo():
	print("Creating files for logo...")
	app_logo_file_url = ""
	splash_image_file_url = ""

	frappe.db.set_value("Website Settings","Website Settings","app_name","Parsimony")
	# app_logo_file_exists = frappe.db.exists("File", {"file_name":["like", "%parsimony_app_logo.png%"],"attached_to_doctype": "Website Settings","attached_to_name": "Website Settings"})
	app_logo_file_exists = frappe.db.sql("""
			SELECT `name` 
			FROM `tabFile` 
			WHERE `file_name`='parsimony_app_logo.png'
			AND `attached_to_doctype` = 'Website Settings'
			AND `attached_to_name` = 'Website Settings'
			LIMIT 1;""",as_dict=True)
	print("App logo file exists:-----------------", app_logo_file_exists)
	if len(app_logo_file_exists)==1:
		app_logo_file_url = frappe.db.get_value("File",app_logo_file_exists,"file_url")
		frappe.db.set_value("Website Settings","Website Settings","app_logo",app_logo_file_url)
		frappe.db.set_value("Website Settings","Website Settings","favicon",app_logo_file_url)
	else:
		app_logo_file_doc = frappe.get_doc({
			"doctype": "File",
			"file_name": "parsimony_app_logo.png",
			"is_private": 0,
			"content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_app_logo.png"), "rb").read(),
			"attached_to_doctype": "Website Settings",
			"attached_to_name": "Website Settings"
		})
		app_logo_file_doc.insert(ignore_permissions=True)
		app_logo_file_url = app_logo_file_doc.file_url
		print("App logo file created.","File Name: ", app_logo_file_doc.name, "File URL:",app_logo_file_doc.file_url)
		frappe.db.set_value("Website Settings","Website Settings","app_logo",app_logo_file_url)
		frappe.db.set_value("Website Settings","Website Settings","favicon",app_logo_file_url)
	

	splash_image_file_exists = frappe.db.exists("File", {"file_name":["like","parsimony_logo_with_name.png"],"attached_to_doctype": "Website Settings","attached_to_name": "Website Settings"})
	print("Splash image file exists:-----------------", splash_image_file_exists)
	if splash_image_file_exists:
		splash_image_file_url = frappe.get_value("File", splash_image_file_exists, "file_url")
		frappe.db.set_value("Website Settings", "Website Settings", "splash_image", splash_image_file_url)  # Update the splash_image field in Website Settings
		frappe.db.set_value("Website Settings", "Website Settings", "banner_image", splash_image_file_url)  # Update the banner_image field in Website Settings
	else:
		splash_image_doc = frappe.get_doc({
			"doctype": "File",
			"file_name": "parsimony_logo_with_name.png",
			"is_private": 0,
			"content": open(frappe.get_app_path("rfs", "public", "images", "parsimony_logo_with_name.png"), "rb").read(),
			"attached_to_doctype": "Website Settings",
			"attached_to_name": "Website Settings"
		})
		splash_image_doc.insert(ignore_permissions=True)
		frappe.db.commit()  # Commit the transaction to ensure the file is saved
		splash_image_file_url = splash_image_doc.file_url
		print("Splash image file created successfully.", "File Name:", splash_image_doc.name, "File URL:", splash_image_doc.file_url)
	
		frappe.db.set_value("Website Settings", "Website Settings", "splash_image", splash_image_file_url)  # Update the splash_image field in Website Settings
		frappe.db.set_value("Website Settings", "Website Settings", "banner_image", splash_image_file_url)  # Update the banner_image field in Website Settings


	##### Create New footer template
	parsimony_footer_template_exists = frappe.db.exists("Web Template",{"name":"Parsimony Footer"})
	if parsimony_footer_template_exists == None:
		footer_template_doc = frappe.new_doc("Web Template")
		footer_template_doc.__newname = "Parsimony Footer"
		footer_template_doc.type = "Footer"
		footer_template_doc.template = f"""
			<div class="footer row fixed-bottom" style="padding-left:6%; background-color: #0A7A83;">
			<div class="col-sm-4" style="padding-top:5px">
				<img src="{app_logo_file_url}" alt="Parsimony Logo" class="brand-logo-img" style="height: 50px; width: 40px" />
				<b><span class="brand-name" style="color:white; font-size: 20px; ">Parsimony</span></b>
				<br>
				
				<p style="color:white; margin-bottom:0px">
					&copy; 2026 Parsimony. Built for businesses that move fast.
				</p>
			</div>

			<div class="col-sm-4" style="padding-top:5px">
				<p style="color:white; margin-bottom:0px;">
					AI chat agents, voice agents, marketing automation, and cloud ERP — built for businesses that want to grow without growing their headcount.
				</p>
			</div>
			<div class="col-sm-4" style="padding-top:5px">
				<div style="text-align: left; padding-left:250px;">
					<!--<h5 class="footer" style="color:white;">Contact Us:</h5>-->
					<p>
						<!--<br>-->
						<!--Email: greycube@edu.in<br>-->
						<span style="color:white;">🌐</span>
						<a href="https://parsimony.com/" style="color:white;">
							parsimony.com
						</a>
						
						<br>
						<span style="color:white;">📞</span>
							<a href="tel:+13072845523" style="color:white; text-decoration:none;">
								+1 (307) 284-5523
							</a>   
				</div>
			</div>
		"""
		footer_template_doc.save(ignore_permissions=True)
		frappe.db.commit()
		print("Parsimony Footer Template is created.----------", footer_template_doc.name)
		frappe.db.set_value("Website Settings", "Website Settings", "footer_template", footer_template_doc.name)
	else :
		print("Template already exists.............")
		frappe.db.set_value("Website Settings", "Website Settings", "footer_template", parsimony_footer_template_exists)