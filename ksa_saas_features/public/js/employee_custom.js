frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        if (frm.is_new()) return;

        const saas = frappe.boot.saas_features || {};

        // 1. Elm Muqeem Button
        if (saas.muqeem && frm.doc.iqama_number) {
            frm.add_custom_button(__('Sync Iqama Status'), function() {
                frappe.call({
                    method: 'ksa_saas_features.api.sync_muqeem_employee',
                    args: { employee_id: frm.doc.name },
                    freeze: true,
                    freeze_message: __('Querying Muqeem Gateway...'),
                    callback: function(r) {
                        if (r.message && r.message.status === "success") {
                            frappe.msgprint({ title: __('Success'), message: r.message.message, indicator: 'green' });
                            frm.reload_doc();
                        }
                    }
                });
            }, __('Government Portals'));
        }

        // 2. CHI Insurance Verification Button
        if (saas.chi && frm.doc.iqama_number) {
            frm.add_custom_button(__('Verify Health Insurance'), function() {
                frappe.call({
                    method: 'ksa_saas_features.api.verify_chi_insurance',
                    args: { employee_id: frm.doc.name },
                    freeze: true,
                    freeze_message: __('Checking CHI / CCHI Policy...'),
                    callback: function(r) {
                        if (r.message && r.message.status === "success") {
                            frappe.msgprint({ title: __('CHI Status'), message: r.message.message, indicator: 'blue' });
                        }
                    }
                });
            }, __('Government Portals'));
        }

        // 3. GOSI & Qiwa Status Check
        if (saas.gosi) {
            frm.add_custom_button(__('Fetch GOSI Details'), function() {
                frappe.msgprint(__('GOSI sync triggered for ') + frm.doc.employee_name);
            }, __('Government Portals'));
        }
    }
});
