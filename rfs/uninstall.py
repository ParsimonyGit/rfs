import frappe

FOOTER_TEMPLATE = "Parsimony Footer"


def before_uninstall():
	"""Drop the Website Settings footer pointer before our Web Template row is deleted.

	`Web Template.module` is a Link to Module Def, so uninstalling this app makes frappe's
	`_delete_linked_documents()` delete the "Parsimony Footer" record along with the module
	(installer.py: v16 :510, v15 :474). `Website Settings.footer_template` would still name
	it, and `get_web_blocks_html()` dereferences that with an unguarded
	`frappe.get_cached_doc("Web Template", ...)` (web_page.py:245) on every page that
	extends base.html -- so the site 502s on every website and Desk route while /api/*
	keeps working. That is the same outage this app already caused once, reached by a
	different route.

	`before_uninstall` runs ahead of `_delete_modules` on both v15 and v16, so clearing the
	pointer here is enough. Leaving the site with frappe's stock footer is the correct
	outcome of removing this app.
	"""
	if frappe.db.get_value("Website Settings", "Website Settings", "footer_template") == FOOTER_TEMPLATE:
		frappe.db.set_value("Website Settings", "Website Settings", "footer_template", "")
		frappe.db.commit()
		print(f"Cleared Website Settings.footer_template (was {FOOTER_TEMPLATE!r})")
