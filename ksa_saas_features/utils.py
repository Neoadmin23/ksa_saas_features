import frappe
from functools import wraps
from frappe.utils import today

def check_feature_access(feature_field):
    """
    Decorator that verifies if the current tenant is entitled to the requested feature.
    Checks toggle status, license expiration, and monthly call quotas.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if frappe.session.user == "Administrator" and getattr(frappe.flags, "in_test", False):
                return fn(*args, **kwargs)

            settings = frappe.get_cached_doc("SaaS Feature Settings")

            # 1. Feature entitlement toggle
            if not getattr(settings, feature_field, 0):
                frappe.throw(
                    frappe._("This government portal integration is not enabled for your account. Please contact support to upgrade."),
                    exc=frappe.PermissionError
                )

            # 2. Expiration check
            if settings.subscription_expiry and str(settings.subscription_expiry) < today():
                frappe.throw(
                    frappe._("Your subscription for this service expired on {0}. Please renew.").format(settings.subscription_expiry),
                    exc=frappe.PermissionError
                )

            # 3. Metered usage quota check
            if settings.api_quota and settings.consumed_api_calls >= settings.api_quota:
                frappe.throw(
                    frappe._("Monthly API call quota exceeded ({0}/{1}). Please upgrade your plan.").format(
                        settings.consumed_api_calls, settings.api_quota
                    ),
                    exc=frappe.PermissionError
                )

            # Increment call count
            settings.db_set("consumed_api_calls", settings.consumed_api_calls + 1)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
