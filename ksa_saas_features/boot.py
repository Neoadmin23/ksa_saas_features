import frappe

def extend_bootinfo(bootinfo):
    """Injects subscription permissions into the global `frappe.boot` object on login."""
    try:
        settings = frappe.get_cached_doc("SaaS Feature Settings")
        bootinfo.saas_features = {
            "muqeem": bool(settings.enable_muqeem),
            "mudad": bool(settings.enable_mudad),
            "gosi": bool(settings.enable_gosi),
            "expiry": str(settings.subscription_expiry) if settings.subscription_expiry else None
        }
    except Exception:
        bootinfo.saas_features = {
            "muqeem": False,
            "mudad": False,
            "gosi": False,
            "expiry": None
        }
