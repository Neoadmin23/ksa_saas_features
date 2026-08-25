import frappe
from frappe.utils import add_days, today, getdate

def daily_compliance_check():
    """
    Daily Cron Job:
    1. Scans for employees with Iqamas expiring within 30 and 60 days.
    2. Logs warnings or creates compliance notifications.
    """
    settings = frappe.get_single("SaaS Feature Settings")

    if not settings.enable_muqeem:
        return

    target_dates = [add_days(today(), 30), add_days(today(), 60)]

    # Fetch employees expiring around 30 or 60 days
    employees = frappe.get_all(
        "Employee",
        filters={
            "status": "Active",
            "custom_identity_type": ["in", ["Identity(Have ID/Iqama No)", "Iqama"]],
            "date_of_retirement": ["in", target_dates]
        },
        fields=["name", "employee_name", "date_of_retirement", "personal_email", "cell_number"]
    )

    for emp in employees:
        frappe.logger("ksa_saas_features").info(
            f"Compliance Alert: Employee {emp.employee_name} ({emp.name}) Iqama nearing expiry on {emp.date_of_retirement}."
        )

def monthly_quota_reset():
    """
    Monthly Cron Job:
    Resets the metered API usage counter on the 1st of every month.
    """
    settings = frappe.get_single("SaaS Feature Settings")
    settings.db_set("consumed_api_calls", 0)
    frappe.logger("ksa_saas_features").info("SaaS Feature Settings: Monthly API call quota reset to 0.")
