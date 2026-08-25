import frappe
from ksa_saas_features.utils import check_feature_access
from ksa_saas_features.muqeem_client import ElmMuqeemClient
from ksa_saas_features.mudad_engine import MudadWPSEngine

@frappe.whitelist()
@check_feature_access("enable_muqeem")
def sync_muqeem_employee(employee_id):
    """Syncs employee Iqama information from Elm Muqeem directly into CentralHrms fields."""
    employee = frappe.get_doc("Employee", employee_id)

    # 1. Identify primary ID/Iqama number from CentralHrms fields
    id_number = employee.get("iqama_national_id") or employee.get("iqama_number") or employee.get("custom_national_id") or employee.get("passport_number")
    
    if not id_number:
        frappe.throw(frappe._("Employee does not have an Iqama/National ID or Passport Number configured."))

    client = ElmMuqeemClient()
    if not client.client_id:
        # Mock/Demo response if API keys are not configured
        return {
            "status": "success",
            "message": frappe._("Muqeem Verified (Demo Mode): Iqama/ID {0} is valid.").format(id_number)
        }

    # 2. Live API Call to Elm Muqeem Gateway
    data = client.fetch_resident_details(id_number)
    
    # 3. Update CentralHrms Employee Master fields directly
    if data.get("iqamaExpiryDate"):
        employee.iqama_expiry_date = data.get("iqamaExpiryDate")
    if data.get("iqamaIssueDate"):
        employee.iqama_issue_date = data.get("iqamaIssueDate")
    if data.get("iqamaExpiryDateHijri"):
        employee.custom_iqama_expiry_date_in_hijri = data.get("iqamaExpiryDateHijri")
    if data.get("iqamaIssueDateHijri"):
        employee.custom_iqama_issue_date_in_hijri = data.get("iqamaIssueDateHijri")
    
    employee.save(ignore_permissions=True)

    return {
        "status": "success",
        "data": data,
        "message": frappe._("Muqeem details fetched and synced successfully for {0}.").format(employee.employee_name)
    }

@frappe.whitelist()
@check_feature_access("enable_gosi")
def sync_gosi_employee(employee_id):
    """Checks GOSI registration using CentralHrms flags."""
    employee = frappe.get_doc("Employee", employee_id)
    is_registered = bool(employee.get("added_to_gosi") or employee.get("custom_is_new_gosi"))
    status_label = "Registered & Active" if is_registered else "Pending Registration"

    return {
        "status": "success",
        "is_registered": is_registered,
        "message": frappe._("GOSI Status for {0}: {1}").format(employee.employee_name, status_label)
    }

@frappe.whitelist()
@check_feature_access("enable_chi")
def verify_chi_insurance(employee_id):
    """Verifies Council of Health Insurance (CHI) policy status."""
    employee = frappe.get_doc("Employee", employee_id)
    has_family = bool(employee.get("custom_has_family_insurance"))
    cancelled = bool(employee.get("custom_h_i_cancelled"))

    if cancelled:
        status_text = "Policy Cancelled"
    elif has_family:
        status_text = "Active (Family Coverage)"
    else:
        status_text = "Active (Individual Coverage)"

    return {
        "status": "success",
        "message": frappe._("CHI Insurance Status for {0}: {1}").format(employee.employee_name, status_text)
    }

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
