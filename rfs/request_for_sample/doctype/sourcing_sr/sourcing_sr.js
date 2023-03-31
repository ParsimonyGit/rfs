// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sourcing SR', {
	onload: function(frm) {
		if(frm.fields_dict['initial_supplier_statistics'] && frm.is_new()==undefined && frm.doc.__onload && "initial_supplier_statistics" in frm.doc.__onload) {
			$(frm.fields_dict['initial_supplier_statistics'].wrapper)
				.html(frappe.render_template('initial_supplier_statistics',{data: frm.doc.__onload}))
		}else{
			$(frm.fields_dict['initial_supplier_statistics'].wrapper).empty().html()
		}	
	},		
	send_email_to_initial_suppliers	: (frm) => {
		if (frm.is_dirty()) {
			frappe.show_alert({ message: __("Save changes to document"), indicator: "orange" });
			return
		}	
		frm.call({
			doc: frm.doc,
			method: 'send_mail_to_initial_supplier',
			freeze: true,
			freeze_message: __('Sending Emails..'),			
			callback: function(r) {
				if (r && r.message) {
					console.log(r)
				}
			}			
		});		
	},
	preview_email_to_initial_suppliers: (frm) => {
		if (frm.is_dirty()) {
			frappe.show_alert({ message: __("Save changes to document"), indicator: "orange" });
			return
		}		
		let dialog = new frappe.ui.Dialog({
			title: __('Preview Email'),
			fields: [
				{
					label: __('Supplier'),
					fieldtype: 'Select',
					fieldname: 'initial_supplier_name',
					options: frm.doc.initial_supplier_details.map(row => row.initial_supplier_name),
					reqd: 1
				},
				{
					fieldtype: 'Column Break',
					fieldname: 'col_break_1',
				},
				{
					label: __('Subject'),
					fieldtype: 'Data',
					fieldname: 'initial_email_subject',
					read_only: 1,
					depends_on: 'initial_email_subject'
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'sec_break_1',
					hide_border: 1
				},
				{
					label: __('Email'),
					fieldtype: 'HTML',
					fieldname: 'email_preview'
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'sec_break_2'
				},
				{
					label: __('Note'),
					fieldtype: 'HTML',
					fieldname: 'note'
				}
			]
		});

		dialog.fields_dict['initial_supplier_name'].df.onchange = () => {
			var initial_supplier_name = dialog.get_value('initial_supplier_name');
			frm.call('get_supplier_email_preview', {initial_supplier_name: initial_supplier_name}).then(result => {
				dialog.fields_dict.email_preview.$wrapper.empty();
				dialog.fields_dict.email_preview.$wrapper.append(result.message);
			});

		}

		dialog.fields_dict.note.$wrapper.append(`<p class="small text-muted">This is a preview of the email to be sent.</p>`);

		dialog.set_value("initial_email_subject", frm.doc.initial_email_subject);
		dialog.show();
	},	
	specification_template: function(frm) {
		if (frm.doc.specification_template) {
			frappe.call({
				method: 'rfs.request_for_sample.doctype.sourcing_sr.sourcing_sr.get_specification_template_details',
				args: {
					specification_template_name: frm.doc.specification_template
				},
				callback: function(r) {
					if(r.message) {
						frm.set_value('specification_details', r.message);
					} else {
						frm.set_value('specification_details', '');
					}
				}
			});			
			
		}
	}
});
