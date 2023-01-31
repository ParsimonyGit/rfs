(() => {
  // ../rfs/rfs/public/js/carrier_rfs_quick_entry.bundle.js
  frappe.provide("frappe.ui.form");
  frappe.ui.form.CarrierRFSQuickEntryForm = class CarrierRFSQuickEntryForm extends frappe.ui.form.QuickEntryForm {
    render_dialog() {
      super.render_dialog();
      let dialog = this.dialog;
      let carrier_account_field = dialog.get_field("carrier_account");
      carrier_account_field.df.get_query = function(params) {
        return {
          filters: {
            "is_group": 0,
            "root_type": "Expense"
          }
        };
      };
    }
  };
})();
//# sourceMappingURL=carrier_rfs_quick_entry.bundle.QABYECQ7.js.map
