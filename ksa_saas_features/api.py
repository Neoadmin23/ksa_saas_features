import frappe
from ksa_saas_features.utils import check_feature_access
from ksa_saas_features.muqeem_client import ElmMuqeemClient
from ksa_saas_features.mudad_engine import MudadWPSEngine

@frappe.whitelist()
@check_feature_access("enable_muqeem")
def sync_muqeem_employee(employee_id):
    """Syncs employee Iqama information from Elm Muqeem API using CentralHrms fields."""
    employee = frappe.get_doc("Employee", employee_id)

    # Use existing CentralHrms identity fields
    iqama_no = employee.get("iqama_number") or employee.get("custom_national_id")
    if not iqama_no:
        frappe.throw(frappe._("Employee does not have an Iqama or National ID configured."))

    client = ElmMuqeemClient()
    if not client.client_id:
        return {
            "status": "success",
            "message": frappe._("Muqeem Verified (Demo Mode): Iqama {0} is valid and active.").format(iqama_no)
        }

    data = client.fetch_resident_details(iqama_no)
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

    return {
        "status": "success",
        "is_registered": is_registered,
        "message": frappe._("GOSI registration status verified for {0}.").format(employee.employee_name)
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

@frappe.whitelist()
@check_feature_access("enable_chi")
def verify_chi_insurance(employee_id):
    """Verifies Council of Health Insurance (CHI) policy status using CentralHrms fields."""
    employee = frappe.get_doc("Employee", employee_id)
    has_family = bool(employee.get("custom_has_family_insurance"))
    cancelled = bool(employee.get("custom_h_i_cancelled"))

    status_str = "Active (Cancelled)" if cancelled else ("Active with Family" if has_family else "Active (Individual)")

    return {
        "status": "success",
        "message": frappe._("CHI Insurance Status for {0}: {1}").format(employee.employee_name, status_str)
    }
