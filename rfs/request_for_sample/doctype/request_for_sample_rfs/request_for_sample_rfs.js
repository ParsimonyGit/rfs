// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request For Sample RFS', {
	proposed_sample_tracking_no: function (frm) {
		if (frm.doc.proposed_sample_tracking_no) {
			let new_status='RFS To Vendor'
			let new_status_datetime_field='rfs_to_vendor_date'
			let new_status_color='orange' // no Pink
			set_status(frm,new_status,new_status_datetime_field,new_status_color)
		}
	},
	shipment_sample_tracking_no: function (frm) {
		if (frm.doc.shipment_sample_tracking_no) {
			let new_status='RFS From Vendor'
			let new_status_datetime_field='rfs_from_vendor_date'
			let new_status_color='orange' // no Purple
			set_status(frm,new_status,new_status_datetime_field,new_status_color)
		}
	},
	rfs_received: function (frm) {
		if (frm.doc.rfs_received==1) {
			let new_status='RFS Received'
			let new_status_datetime_field='rfs_received_date'
			let new_status_color='blue'
			set_status(frm,new_status,new_status_datetime_field,new_status_color)
		}
	},
	rfs_reviewed_by: function (frm) {
		if (frm.doc.rfs_reviewed_by!=undefined || frm.doc.rfs_reviewed_by!='') {
			let new_status='RFS In Review'
			let new_status_datetime_field='rfs_in_review_date'
			let new_status_color='yellow'
			set_status(frm,new_status,new_status_datetime_field,new_status_color)
		}
	},
	status: function (frm) {
		
		let valid_action_status=['RFS Approved','RFS Rejected','RFS Canceled']
		if (valid_action_status.includes(frm.doc.status)) {
			if (frm.doc.rfs_in_review_date==undefined || frm.doc.rfs_in_review_date=='') {
				frappe.throw(__('Status {0} cannot be set. As RFS  has not passed through <b>RFS In Review</b> stage.',[frm.doc.status]))
				return
			}			
			let new_status=frm.doc.status
			let new_status_datetime_field
			let new_status_color
			if (new_status=='RFS Approved') {
				new_status_datetime_field='rfs_approved_date'
				new_status_color='green'
			} else if(new_status=='RFS Rejected') {
				new_status_datetime_field='rfs_rejected_date'
				new_status_color='red'				
			} else if(new_status=='RFS Canceled') {
				new_status_datetime_field='rfs_canceled_date'
				new_status_color='red'		 // no gray		
			}
			set_status(frm,new_status,new_status_datetime_field,new_status_color)
		}
	},	
	onload: function(frm) {
		if(frm.fields_dict['rfs_status_history'] && frm.is_new()==undefined && frm.doc.__onload && "status_history" in frm.doc.__onload) {
			$(frm.fields_dict['rfs_status_history'].wrapper)
				.html(frappe.render_template('request_for_sample_status_history',{data: frm.doc.__onload}))
		}else{
			$(frm.fields_dict['rfs_status_history'].wrapper).empty().html()
		}	
	},	
	onload_post_render: function (frm) {
		const default_company = frappe.defaults.get_default('company');
		frm.set_query('company_address', function(doc) {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: frappe.defaults.get_default('company')
				}
			};
		});		
		
	},
	supplier: function(frm) {
		frm.set_query('supplier_address', address_query('Supplier',frm.doc.supplier));
	},
	supplier_address:function (frm) {
		frappe.call('rfs.request_for_sample.doctype.request_for_sample_rfs.request_for_sample_rfs.get_supplier_address_html', {
			address: frm.doc.supplier_address
		}).then(r => {
			frm.set_value('proposed_sample_sent_to', r.message)
		})
	},
	company_address(frm) {
		if(frm.doc.company_address) {
			frappe.call({
				method: "frappe.contacts.doctype.address.address.get_address_display",
				args: {"address_dict": frm.doc.company_address },
				callback: function(r) {
					if(r.message) {
						me.frm.set_value("proof_shipment_sample_sent_to", r.message)
					}
				}
			})
		} else {
			frm.set_value("proof_shipment_sample_sent_to", "");
		}
	},	
	refresh: function(frm) {
		if (!frm.doc.__islocal && frm.doc.our_sample_pictures && frm.doc.our_sample_pictures.length > 0) {
			$(frm.fields_dict.proposed_sample_pictures_display.wrapper).empty().html(
				frappe.render_template('display_image', {
					data: frm.doc.our_sample_pictures
				})
			)
		}else{
			$(frm.fields_dict.proposed_sample_pictures_display.wrapper).empty().html()
		}
		if (!frm.doc.__islocal && frm.doc.factory_sample_pictures && frm.doc.factory_sample_pictures.length > 0) {
			$(frm.fields_dict.shipment_sample_pictures_display.wrapper).empty().html(
				frappe.render_template('display_image', {
					data: frm.doc.factory_sample_pictures
				})
			)
		}else{
			$(frm.fields_dict.shipment_sample_pictures_display.wrapper).empty().html()
		}		
		if(!frm.doc.__islocal && frm.doc.create_label &&  frm.doc.create_label.length>0 ) {
			let data=frm.doc.create_label
			let result= data.replaceAll('\n', '<br/>');
			// result= result+'<br/>'+frm.doc.name
			$(frm.fields_dict.label_requirements.wrapper).empty().html(
				`<div class="container">
				<div class="row">
					<div class="col-sm">
						<div class="card text-center">
							<h5 class="card-header">${frm.doc.project}:${frm.doc.project_name_sidemark}</h5>
							<div class="card-body">
							  <div class="card-text text-left">${result}</div>
							</div>
							<h5 class="card-footer">${frm.doc.name}</h5>
						</div>
					</div>
				</div>
			</div>`
			);
			}else{
				$(frm.fields_dict.label_requirements.wrapper).empty().html()
			}		
	},
	add_from_email_groups: function(frm) {
		frappe.prompt({
			label: 'Select Email Group',
			fieldname: 'email_group',
			fieldtype: 'Link',
			options: 'Email Group'
		}, (values) => {
			frappe.db.get_list('Email Group Member', {
				fields: ['email'],
				filters: {
					'unsubscribed': 0,
					'email_group':values.email_group
				}
			}).then(records => {
				let email_list = $.map(records, (row, idx)=>{ return row.email}).toString()	
				email_list= email_list.replaceAll(',', ',\n');
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
	form_render: function(frm, cdt, cdn){
		frm.meta.make_attachments_public=1
		$("button[data-fieldname='attach_sample_image']").css({ 'background-color' : '#6da0f2'});
	},
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
			frappe.model.set_value(cdt, cdn, 'photo_id', filename);	
		}
	},
	factory_sample_pictures_add: function(frm, cdt, cdn){
		let child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'photo_id', "Photo "+child.idx);
	}
});

function address_query(doctype,fieldname) {
		return {
			query: 'frappe.contacts.doctype.address.address.address_query',
			filters: {
				'link_doctype': doctype,
				'link_name': cur_frm.doc.supplier
			}
		};
}

function set_status(frm,new_status,new_status_datetime_field,new_status_color) {
	frm.set_value(new_status_datetime_field, frappe.datetime.now_datetime())
	let earlier_status=frm.doc.status
	frm.set_value('status',new_status )
	frappe.show_alert({
		message:__('Status is changed from {0} to <b>{1}</b>',[earlier_status,new_status]),
		indicator:new_status_color
	}, 8);	
}