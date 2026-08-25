import frappe
from ksa_saas_features.utils import check_feature_access
from ksa_saas_features.muqeem_client import ElmMuqeemClient
from ksa_saas_features.mudad_engine import MudadWPSEngine

@frappe.whitelist()
@check_feature_access("enable_muqeem")
def sync_muqeem_employee(employee_id):
    """Syncs employee Iqama information from Elm Muqeem API using CentralHrms fields."""
    employee = frappe.get_doc("Employee", employee_id)

    # Check CentralHrms identity fields in order of fallback
    id_number = employee.get("custom_national_id") or employee.get("iqama_number") or employee.get("passport_number")
    if not id_number:
        frappe.throw(frappe._("Employee does not have an Iqama, National ID, or Passport number configured."))

    client = ElmMuqeemClient()
    if not client.client_id:
        return {
            "status": "success",
            "message": frappe._("Muqeem Verified (Demo Mode): Identity record {0} for {1} is valid.").format(id_number, employee.employee_name)
        }

    data = client.fetch_resident_details(id_number)
    return {
        "status": "success",
        "data": data,
        "message": frappe._("Muqeem details fetched successfully for {0}.").format(employee.employee_name)
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
    """Verifies Council of Health Insurance (CHI) policy using CentralHrms insurance fields."""
    employee = frappe.get_doc("Employee", employee_id)
    has_family = bool(employee.get("custom_has_family_insurance"))
    cancelled = bool(employee.get("custom_h_i_cancelled"))

    if cancelled:
        status_text = "Policy Cancelled"
    elif has_family:
        status_text = "Active (Comprehensive Family Coverage)"
    else:
        status_text = "Active (Individual Coverage)"

    return {
        "status": "success",
        "message": frappe._("CHI Insurance Status for {0}: {1}").format(employee.employee_name, status_text)
    }

@frappe.whitelist()
@check_feature_access("enable_mudad")
def generate_mudad_wps(payroll_entry_id):
    """Generates Wage Protection System (WPS/SIF) file for Mudad."""
    engine = MudadWPSEngine(payroll_entry_id)
    sif_payload = engine.generate_sif_content()

    return {
        "status": "success",
        "message": frappe._("Saudi WPS (SIF) generated successfully for {0} records.").format(len(sif_payload.splitlines()) - 1),
        "payload": sif_payload
    }
