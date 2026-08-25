app_name = "ksa_saas_features"
app_title = "KSA SaaS Features"
app_publisher = "Your Company"
app_description = "SaaS Feature Gating and KSA Government Portals"
app_email = "dev@yourdomain.com"
app_license = "MIT"

extend_bootinfo = "ksa_saas_features.boot.extend_bootinfo"

doctype_js = {
    "Employee": "public/js/employee_custom.js",
    "Payroll Entry": "public/js/payroll_entry_custom.js"
}

scheduler_events = {
    "monthly": [
        "ksa_saas_features.tasks.monthly_quota_reset"
    ]
}
