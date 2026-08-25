frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        if (frm.is_new()) return;

        const saas = frappe.boot.saas_features || {};
        const has_id = frm.doc.custom_national_id || frm.doc.iqama_number || frm.doc.passport_number;

        // 1. Elm Muqeem Button
        if (saas.muqeem && has_id) {
            frm.add_custom_button(__('Sync Iqama Status'), function() {
                frappe.call({
                    method: 'ksa_saas_features.api.sync_muqeem_employee',
                    args: { employee_id: frm.doc.name },
                    freeze: true,
                    freeze_message: __('Querying Muqeem Gateway...'),
                    callback: function(r) {
                        if (r.message && r.message.status === "success") {
                            frappe.msgprint({ title: __('Muqeem Status'), message: r.message.message, indicator: 'green' });
                            frm.reload_doc();
                        }
                    }
                });
            }, __('Government Portals'));
        }

        // 2. CHI Insurance Verification Button
        if (saas.chi) {
            frm.add_custom_button(__('Verify Health Insurance'), function() {
                frappe.call({
                    method: 'ksa_saas_features.api.verify_chi_insurance',
                    args: { employee_id: frm.doc.name },
                    freeze: true,
                    freeze_message: __('Checking CHI / CCHI Policy...'),
                    callback: function(r) {
                        if (r.message && r.message.status === "success") {
                            frappe.msgprint({ title: __('CHI Insurance'), message: r.message.message, indicator: 'blue' });
                        }
                    }
                });
            }, __('Government Portals'));
        }

        // 3. GOSI Verification Button
        if (saas.gosi) {
            frm.add_custom_button(__('Fetch GOSI Details'), function() {
                frappe.call({
                    method: 'ksa_saas_features.api.sync_gosi_employee',
                    args: { employee_id: frm.doc.name },
                    freeze: true,
                    freeze_message: __('Verifying GOSI Status...'),
                    callback: function(r) {
                        if (r.message && r.message.status === "success") {
                            frappe.msgprint({ title: __('GOSI Status'), message: r.message.message, indicator: 'green' });
                        }
                    }
                });
            }, __('Government Portals'));
        }
    }
});
