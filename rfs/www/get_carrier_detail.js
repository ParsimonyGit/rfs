frappe.ready(function() {

	if(frappe.utils.get_url_arg('subject')) {
	  $('[name="subject"]').val(frappe.utils.get_url_arg('subject'));
	}

	$('.btn-send').off("click").on("click", function() {
        console.log(2222)
        var rfs_name=$('[data-fieldname="rfs_name"]').val();
		var shipment_sample_carrier_name = $('[data-fieldname="shipment_sample_carrier_name"]').val();
		var shipment_sample_tracking_no = $('[data-fieldname="shipment_sample_tracking_no"]').val();
        console.log(rfs_name,shipment_sample_carrier_name,shipment_sample_tracking_no)
		// if(!(email && message)) {
		// 	frappe.msgprint('{{ _("Please enter both your email and message so that we can get back to you. Thanks!") }}');
		// 	return false;
		// }

		// if(!validate_email(email)) {
		// 	frappe.msgprint('{{ _("You seem to have written your name instead of your email. Please enter a valid email address so that we can get back.") }}');
		// 	$('[name="email"]').focus();
		// 	return false;
		// }
        // let appointment =  frappe.call({
        //     method: 'erpnext.www.book_appointment.index.create_appointment',
        //     args: {
        //         'date': window.selected_date,
        //         'time': window.selected_time,
        //         'contact': contact,
        //         'tz':window.selected_timezone
        //     },
        //     callback: (response)=>{
        //         if (response.message.status == "Unverified") {
        //             frappe.show_alert("Please check your email to confirm the appointment")
        //         } else {
        //             frappe.show_alert("Appointment Created Successfully");
        //         }
        //         setTimeout(()=>{
        //             let redirect_url = "/";
        //             if (window.appointment_settings.success_redirect_url){
        //                 redirect_url += window.appointment_settings.success_redirect_url;
        //             }
        //             window.location.href = redirect_url;},5000)
        //     },
        //     error: (err)=>{
        //         frappe.show_alert("Something went wrong please try again");
        //         button.disabled = false;
        //     }
        // });

		$("#contact-alert").toggle(false);
        frappe.call("rfs.www.get_carrier_detail.send_carrier_details", {
			rfs_name: rfs_name,
			shipment_sample_carrier_name: shipment_sample_carrier_name,
			shipment_sample_tracking_no: shipment_sample_tracking_no,
            callback: function(r) {
				if(r.message==="okay") {
					frappe.msgprint('{{ _("Thank you for your message") }}');
				} else {
					frappe.msgprint('{{ _("There were errors") }}');
					console.log(r.exc);
				}
				$(':input').val('');
			}
        })

	// 	frappe.send_carrier_details({
	// 		rfs_name: rfs_name,
	// 		shipment_sample_carrier_name: shipment_sample_carrier_name,
	// 		shipment_sample_tracking_no: shipment_sample_tracking_no,
	// 		callback: function(r) {
	// 			if(r.message==="okay") {
	// 				frappe.msgprint('{{ _("Thank you for your message") }}');
	// 			} else {
	// 				frappe.msgprint('{{ _("There were errors") }}');
	// 				console.log(r.exc);
	// 			}
	// 			$(':input').val('');
	// 		}
	// 	}, this);
		return false;
	});

});
