frappe.views.calendar["Request For Sample RFS"] = {
	field_map: {
		"start": "creation",
		"end": "rfs_emailed_date",
		"id": "name",
		"title": "status",
		"allDay": "allDay",
		"progress": "progress"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"label": __("Project")
		}
	],
	get_events_method: "frappe.desk.calendar.get_events"
}
