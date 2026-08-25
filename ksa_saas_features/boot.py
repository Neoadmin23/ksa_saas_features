import frappe

def extend_bootinfo(bootinfo):
    """Injects subscription permissions for all Saudi HR portals into frappe.boot."""
    try:
        settings = frappe.get_cached_doc("SaaS Feature Settings")
        bootinfo.saas_features = {
            "muqeem": bool(settings.enable_muqeem),
            "mudad": bool(settings.enable_mudad),
            "gosi": bool(settings.enable_gosi),
            "qiwa": bool(settings.get("enable_qiwa")),
            "chi": bool(settings.get("enable_chi")),
            "expiry": str(settings.subscription_expiry) if settings.subscription_expiry else None
        }
    except Exception:
        bootinfo.saas_features = {
            "muqeem": False,
            "mudad": False,
            "gosi": False,
            "qiwa": False,
            "chi": False,
            "expiry": None
        }
