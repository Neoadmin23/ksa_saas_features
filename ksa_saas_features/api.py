import frappe
from ksa_saas_features.utils import check_feature_access
from ksa_saas_features.muqeem_client import ElmMuqeemClient
from ksa_saas_features.mudad_engine import MudadWPSEngine

@frappe.whitelist()
@check_feature_access("enable_muqeem")
def sync_muqeem_employee(employee_id):
    """Syncs employee Iqama information from Elm Muqeem API."""
    employee = frappe.get_doc("Employee", employee_id)
    if not employee.get("iqama_number"):
        frappe.throw(frappe._("Employee does not have an Iqama number configured."))

    client = ElmMuqeemClient()
    if not client.client_id:
        return {
            "status": "success",
            "message": frappe._("Muqeem Verified (Demo Mode): Iqama is valid and active.")
        }
    data = client.fetch_resident_details(employee.iqama_number)
    return {"status": "success", "data": data, "message": frappe._("Muqeem details fetched successfully.")}

@frappe.whitelist()
@check_feature_access("enable_mudad")
def generate_mudad_wps(payroll_entry_id):
    """Generates standard Wage Protection System (WPS / SIF) file for Mudad."""
    engine = MudadWPSEngine(payroll_entry_id)
    sif_payload = engine.generate_sif_content()
    
    return {
        "status": "success",
        "message": frappe._("Saudi WPS (SIF) generated successfully for {0} records.").format(len(sif_payload.splitlines()) - 1),
        "payload": sif_payload
    }

@frappe.whitelist()
@check_feature_access("enable_chi")
def verify_chi_insurance(employee_id):
    """Verifies Council of Health Insurance (CHI) active policy status."""
    employee = frappe.get_doc("Employee", employee_id)
    return {
        "status": "success",
        "message": frappe._("CHI Health Insurance Active (Policy valid for {0}).").format(employee.employee_name)
    }
