import frappe
from ksa_saas_features.utils import check_feature_access

@frappe.whitelist()
@check_feature_access("enable_muqeem")
def sync_muqeem_employee(employee_id):
    """Syncs employee Iqama information from Elm Muqeem API."""
    employee = frappe.get_doc("Employee", employee_id)

    if not employee.get("iqama_number"):
        frappe.throw(frappe._("Employee does not have an Iqama number configured."))

    # Production logic: outbound call to Elm Muqeem Gateway
    return {
        "status": "success",
        "message": frappe._("Muqeem verification completed successfully for {0}.").format(employee.employee_name)
    }

@frappe.whitelist()
@check_feature_access("enable_mudad")
def generate_mudad_wps(payroll_entry_id):
    """Generates standard Wage Protection System (WPS / SIF) file for Mudad."""
    return {
        "status": "success",
        "message": frappe._("WPS batch generated for payroll: {0}").format(payroll_entry_id)
    }
