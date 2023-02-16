frappe.ready(function() {

	$('.btn-send').off("click").on("click", function() {
		var rfs_name=$('[data-fieldname="rfs_name"]').val();
		var shipment_sample_carrier_name = $('[data-fieldname="shipment_sample_carrier_name"]').val();
		var shipment_sample_tracking_no = $('[data-fieldname="shipment_sample_tracking_no"]').val();
		var sample_from_vendor_remark=$('[data-fieldname="sample_from_vendor_remark"]').val();

		if(!(rfs_name)) {
			frappe.msgprint('Please use correct RFS name. Click on the received link again. Thanks!');
			return false;
		}
		if(!(shipment_sample_carrier_name)) {
			frappe.msgprint('Please enter carrier name. Thanks!');
			return false;
		}		
		if(!(shipment_sample_tracking_no)) {
			frappe.msgprint('Please enter tracking no. Thanks!');
			return false;
		}		
		$("#contact-alert").toggle(false);

		frappe.call({
			method: 'rfs.www.get_carrier_detail.send_carrier_details',
			args: {
				rfs_name: rfs_name,
				shipment_sample_carrier_name: shipment_sample_carrier_name,
				shipment_sample_tracking_no: shipment_sample_tracking_no,
				sample_from_vendor_remark:sample_from_vendor_remark,				
			},
			// disable the button until the request is completed
			btn: $('.primary-action'),
			// freeze the screen until the request is completed
			freeze: true,
			callback: (r) => {
				if(r.message==="okay") {
					frappe.msgprint('Thank you, we have received your carrier/post details.');
				} else {
					frappe.msgprint(r.message);
					console.log(r.exc);
				}
				// on success
			},
			error: (r) => {
				console.log(r)
				// on error
			}
		})
		
		return false;
	});

});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}