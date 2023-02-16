frappe.views.calendar["Request For Sample RFS"] = {
	field_map: {
		"start": "from_time",
		"end": "to_time",
		"id": "name",
		"title": "subject",
		"color": "color",
		"allDay": "allDay",
		"progress": "progress"
	},
	gantt: {
		field_map: {
			"start": "creation",
			"end": "modified",
			"id": "name",
			"title": "name",
			"color": "color",
			"allDay": "allDay",
			"progress": "progress",
		}
	},
	get_events_method: "rfs.request_for_sample.doctype.request_for_sample_rfs.request_for_sample_rfs.get_rfs_details"
};
