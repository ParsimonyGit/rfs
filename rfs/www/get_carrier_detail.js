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


        let file = $('#factory_sample_picture').prop('files')[0] || {};
        if (file && file.name) {
            file = {
                file_obj: file,
                name: file.name,
                is_private: true,
                folder: 'Home',
            }
        }
		let form_data = new FormData();
		form_data.append("rfs_name", rfs_name)
		form_data.append("shipment_sample_carrier_name", shipment_sample_carrier_name)
		form_data.append("shipment_sample_tracking_no", shipment_sample_tracking_no)
		form_data.append("sample_from_vendor_remark", sample_from_vendor_remark)
		if (file && file.name) {
			// attach file if present
			if (file.file_obj) {
				form_data.append('file', file.file_obj, file.name);
				form_data.append('is_private', +file.private);
				form_data.append('folder', file.folder);

			}

		}		

        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();
            xhr.upload.addEventListener('loadstart', (e) => {
                file.uploading = true;
            })
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    file.progress = e.loaded;
                    file.total = e.total;
                }
            })
            xhr.upload.addEventListener('load', (e) => {
                file.uploading = false;
                resolve();
            })
            xhr.addEventListener('error', (e) => {
                file.failed = true;
                reject();
            })
            xhr.onreadystatechange = () => {
                if (xhr.readyState == XMLHttpRequest.DONE) {

                    console.log(xhr.responseText);
					let result=JSON.parse(xhr.responseText)
					console.log(result,result.message,result.message=="okay")
					if(result.message=="okay") {
						frappe.msgprint('Thank you, we have received your carrier/post details.');
					} else {
						frappe.msgprint(result.message);
						console.log(result.exc);
					}

                    if (xhr.status === 200) {

                        let r = null;
                        let file_doc = null;
                        try {
                            r = JSON.parse(xhr.responseText);
                            if (r.message.doctype === 'File') {
                                file_doc = r.message;
                            }
                        } catch (e) {
                            r = xhr.responseText;
                        }

                        file.doc = file_doc;

                        if (this.on_success) {
                            this.on_success(file_doc, r);
                        }
                    } else if (xhr.status === 403) {
                        let response = JSON.parse(xhr.responseText);
                        frappe.msgprint({
                            title: __('Not permitted'),
                            indicator: 'red',
                            message: response._error_message
                        });
                    } else {
                        file.failed = true;
                        let error = null;
                        try {
                            error = JSON.parse(xhr.responseText);
                        } catch (e) {
                            // pass
                        }
                        // frappe.request.cleanup({}, error);   
                    }
                }
            }
            xhr.open('POST', '/api/method/rfs.www.get_carrier_detail.send_carrier_details', true);
            xhr.setRequestHeader('Accept', 'application/json');



            xhr.send(form_data);
        });			

		// frappe.call({
		// 	method: 'rfs.www.get_carrier_detail.send_carrier_details',
		// 	args: {
		// 		rfs_name: rfs_name,
		// 		shipment_sample_carrier_name: shipment_sample_carrier_name,
		// 		shipment_sample_tracking_no: shipment_sample_tracking_no,
		// 		sample_from_vendor_remark:sample_from_vendor_remark,				
		// 	},
		// 	// disable the button until the request is completed
		// 	btn: $('.primary-action'),
		// 	// freeze the screen until the request is completed
		// 	freeze: true,
		// 	callback: (r) => {
		// 		if(r.message==="okay") {
		// 			frappe.msgprint('Thank you, we have received your carrier/post details.');
		// 		} else {
		// 			frappe.msgprint(r.message);
		// 			console.log(r.exc);
		// 		}
		// 		// on success
		// 	},
		// 	error: (r) => {
		// 		console.log(r)
		// 		// on error
		// 	}
		// })
		
		return false;
	});

});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}