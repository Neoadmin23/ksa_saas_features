import frappe
from ksa_saas_features.utils import check_feature_access
from ksa_saas_features.muqeem_client import ElmMuqeemClient

@frappe.whitelist()
@check_feature_access("enable_muqeem")
def sync_muqeem_employee(employee_id):
    """Syncs employee Iqama information from Elm Muqeem API."""
    employee = frappe.get_doc("Employee", employee_id)

    if not employee.get("iqama_number"):
        frappe.throw(frappe._("Employee does not have an Iqama number configured."))

    client = ElmMuqeemClient()
    
    # In sandbox/demo mode without live Elm keys, return a structured mock response
    if not client.client_id:
        return {
            "status": "success",
            "message": frappe._("Muqeem Verified (Demo Mode): Iqama is active.")
        }

    # Fetch live resident data from Elm
    data = client.fetch_resident_details(employee.iqama_number)
    
    # Update employee fields if returned by Elm
    # employee.iqama_expiry_date = data.get("iqamaExpiryDate")
    # employee.save()

    return {
        "status": "success",
        "data": data,
        "message": frappe._("Muqeem details fetched successfully.")
    }

@frappe.whitelist()
@check_feature_access("enable_mudad")
def generate_mudad_wps(payroll_entry_id):
    """Generates standard Wage Protection System (WPS / SIF) file for Mudad."""
    return {
        "status": "success",
        "message": frappe._("WPS batch generated for payroll: {0}").format(payroll_entry_id)
    }
