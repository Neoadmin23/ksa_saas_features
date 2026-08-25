frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        if (frappe.boot.saas_features && frappe.boot.saas_features.muqeem) {
            if (frm.doc.iqama_number && !frm.is_new()) {
                frm.add_custom_button(__('Sync Iqama Status'), function() {
                    frappe.call({
                        method: 'ksa_saas_features.api.sync_muqeem_employee',
                        args: {
                            employee_id: frm.doc.name
                        },
                        freeze: true,
                        freeze_message: __('Connecting to Elm Muqeem Gateway...'),
                        callback: function(r) {
                            if (r.message && r.message.status === "success") {
                                frappe.msgprint({
                                    title: __('Success'),
                                    message: r.message.message,
                                    indicator: 'green'
                                });
                                frm.reload_doc();
                            }
                        }
                    });
                }, __('Government Portals'));
            }
        }
    }
});
