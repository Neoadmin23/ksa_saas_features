import frappe
from frappe.utils import add_days, today

def send_expiry_and_quota_alerts():
    """
    Sends alerts for:
    1. Employees with Iqamas expiring in 30 days.
    2. SaaS API Quota reaching 90% consumption.
    """
    settings = frappe.get_single("SaaS Feature Settings")
    
    # Check API Quota Warning
    if settings.api_quota and settings.consumed_api_calls:
        if (settings.consumed_api_calls / settings.api_quota) >= 0.90:
            frappe.sendmail(
                recipients=["Administrator"],
                subject="SaaS API Quota Warning: 90% Consumed",
                message=f"Your monthly API quota ({settings.consumed_api_calls}/{settings.api_quota}) is nearly exhausted."
            )

    # Check Document Expiries (Muqeem / Iqama)
    expiry_threshold = add_days(today(), 30)
    expiring_employees = frappe.get_all(
        "Employee",
        filters={"status": "Active", "iqama_expiry_date": expiry_threshold},
        fields=["name", "employee_name", "iqama_expiry_date"]
    )

    for emp in expiring_employees:
        frappe.logger("ksa_saas_features").warning(
            f"Alert: Employee {emp.employee_name} ({emp.name}) Iqama expires on {emp.iqama_expiry_date}."
        )
