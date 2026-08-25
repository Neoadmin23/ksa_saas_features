app_name = "ksa_saas_features"
app_title = "KSA SaaS Features"
app_publisher = "Your Company"
app_description = "SaaS Feature Gating and KSA Government Portals"
app_email = "dev@yourdomain.com"
app_license = "MIT"

# Extend bootinfo to pass feature flags to browser session
extend_bootinfo = "ksa_saas_features.boot.extend_bootinfo"

# Attach client-side scripts to standard DocTypes
doctype_js = {
    "Employee": "public/js/employee_custom.js"
}
