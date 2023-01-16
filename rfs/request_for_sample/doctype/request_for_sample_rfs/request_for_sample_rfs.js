// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request For Sample RFS', {
	supplier_address:function (frm) {
		frappe.call('rfs.request_for_sample.doctype.request_for_sample_rfs.request_for_sample_rfs.get_supplier_address_html', {
			address: frm.doc.supplier_address
		}).then(r => {
			// $(frm.fields_dict.label_requirements.wrapper).empty().html(r.message);
			frm.set_value('proposed_sample_sent_to', r.message)
		})
	},
	supplier: function (frm) {
		frappe.db.get_list('Dynamic Link', {
			fields: ['parent'],
			filters: {
				link_doctype: 'Supplier',
				link_name: frm.doc.supplier,
				parenttype: 'Address',
				parentfield: 'links'
			},
			as_list: 1
		}).then(records => {
			if (records && records.length > 0) {
				let filter_add = records.flat()
				frm.set_query('supplier_address', () => {
					return {
						filters: {
							name: ['in', filter_add]
						}
					}
				})
			}
		})

	},
	refresh: function(frm) {
		if (!frm.doc.__islocal && frm.doc.our_sample_pictures && frm.doc.our_sample_pictures.length > 0) {
			$(frm.fields_dict.proposed_sample_pictures_display.wrapper).empty().html(
				frappe.render_template('display_image', {
					data: frm.doc.our_sample_pictures
				})
			)
		}
		if (!frm.doc.__islocal && frm.doc.factory_sample_pictures && frm.doc.factory_sample_pictures.length > 0) {
			$(frm.fields_dict.shipment_sample_pictures_display.wrapper).empty().html(
				frappe.render_template('display_image', {
					data: frm.doc.factory_sample_pictures
				})
			)
		}		
		if(!frm.doc.__islocal && frm.doc.create_label &&  frm.doc.create_label.length>0 ) {
			let data=frm.doc.create_label
			let result= data.replaceAll('\n', '<br/>');
			console.log('result',result)
			$(frm.fields_dict.label_requirements.wrapper).empty().html(
				`<div class="container">
				<div class="row">
					<div class="col-sm">
						<div class="card text-center">
							<h5 class="card-header">${frm.doc.project}:${frm.doc.project_name_sidemark}</h5>
							<div class="card-body">
							  <div class="card-text text-left">${result}</div>
							</div>
						</div>
					</div>
				</div>
			</div>`
			);
			}		
	},
	add_from_email_groups: function(frm) {
		frappe.prompt({
			label: 'Select Email Group',
			fieldname: 'email_group',
			fieldtype: 'Link',
			options: 'Email Group'
		}, (values) => {
			console.log(values.email_group);
			frappe.db.get_list('Email Group Member', {
				fields: ['email'],
				filters: {
					'unsubscribed': 0,
					'email_group':values.email_group
				}
			}).then(records => {
				console.log(records);
				let email_list = $.map(records, (row, idx)=>{ return row.email}).toString()	
				email_list= email_list.replaceAll(',', ',\n');
				console.log('email_list',email_list);
				if (frm.doc.email && frm.doc.email.length>0){
					email_list=','+email_list
					frm.set_value('email', frm.doc.email+email_list)
				}else{
					frm.set_value('email', email_list)
				}	
				
			})
			
		})		
	},
	sample_template: function(frm) {
		if (frm.doc.sample_template) {
			frappe.call({
				method: 'rfs.request_for_sample.doctype.request_for_sample_rfs.request_for_sample_rfs.get_sample_template_details',
				args: {
					sample_template_name: frm.doc.sample_template
				},
				callback: function(r) {
					if(r.message) {
						frm.set_value('sample_details', r.message);
					} else {
						frm.set_value('sample_details', '');
					}
				}
			});			
			
		}
	}
});

frappe.ui.form.on('Samples RFS', {
	our_sample_pictures_add: function(frm, cdt, cdn){
		let child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'photo_id', "Photo "+child.idx);
	},
	attach_sample_image: function(frm, cdt, cdn){
		let child = locals[cdt][cdn];
		if (child.attach_sample_image){
			let attached_filname=child.attach_sample_image
			let filename_start_index=attached_filname.lastIndexOf('/')
			let filename_end_index=attached_filname.lastIndexOf('.')
			let filename=attached_filname.slice(filename_start_index+1,filename_end_index)
			console.log(filename)		
			frappe.model.set_value(cdt, cdn, 'photo_id', filename);	
		}
	},
	factory_sample_pictures_add: function(frm, cdt, cdn){
		let child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'photo_id', "Photo "+child.idx);
	}
});