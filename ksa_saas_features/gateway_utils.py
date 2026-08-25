import frappe
from frappe import _

def log_and_meter_gateway_call(gateway_name, success=True, error_message=None):
    """Meters API quota and logs gateway activity."""
    settings = frappe.get_single("SaaS Feature Settings")
    logger = frappe.logger("ksa_saas_features")

    # 1. Check Quota Limit
    if settings.api_quota and settings.consumed_api_calls >= settings.api_quota:
        logger.warning(f"Gateway Blocked: Monthly quota exhausted for {gateway_name}")
        frappe.throw(_("Monthly API Gateway Quota exhausted ({0}/{1}).").format(
            settings.consumed_api_calls, settings.api_quota
        ))

    # 2. Increment Metered Usage
    settings.db_set("consumed_api_calls", settings.consumed_api_calls + 1)

    # 3. File Logging
    if success:
        logger.info(f"Gateway Success [{gateway_name}]: Call recorded. Total consumed: {settings.consumed_api_calls}")
    else:
        logger.error(f"Gateway Failure [{gateway_name}]: {error_message}")
