frappe.ui.form.on('Payroll Entry', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) { // Submitted payroll
            const saas = frappe.boot.saas_features || {};

            if (saas.mudad) {
                frm.add_custom_button(__('Generate Mudad WPS (SIF)'), function() {
                    frappe.call({
                        method: 'ksa_saas_features.api.generate_mudad_wps',
                        args: { payroll_entry_id: frm.doc.name },
                        freeze: true,
                        freeze_message: __('Generating Saudi WPS File...'),
                        callback: function(r) {
                            if (r.message && r.message.status === "success") {
                                frappe.msgprint({
                                    title: __('Mudad WPS File Ready'),
                                    message: r.message.message,
                                    indicator: 'green'
                                });
                            }
                        }
                    });
                }, __('Saudi Compliance'));
            }
        }
    }
});
