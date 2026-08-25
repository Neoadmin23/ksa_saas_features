import frappe
import requests

class ElmMuqeemClient:
    """Client for interacting with Elm Muqeem REST Gateway."""
    
    SANDBOX_URL = "https://api-sandbox.elm.sa/muqeem/v1"
    PROD_URL = "https://api.elm.sa/muqeem/v1"

    def __init__(self):
        self.settings = frappe.get_single("SaaS Feature Settings")
        self.base_url = self.PROD_URL if self.settings.muqeem_environment == "Production" else self.SANDBOX_URL
        self.client_id = self.settings.muqeem_client_id
        self.client_secret = self.settings.get_password("muqeem_client_secret")
        self.api_key = self.settings.get_password("muqeem_api_key")
        self.establishment_id = self.settings.muqeem_establishment_id

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "client-id": self.client_id or "",
            "client-secret": self.client_secret or "",
            "apiKey": self.api_key or ""
        }

    def fetch_resident_details(self, iqama_number):
        """Query resident status, expiry, and profession."""
        url = f"{self.base_url}/establishments/{self.establishment_id}/residents/{iqama_number}"
        
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=20)
            if response.status_code == 200:
                return response.json()
            else:
                frappe.throw(frappe._("Elm Muqeem Error ({0}): {1}").format(response.status_code, response.text))
        except requests.exceptions.RequestException as e:
            frappe.throw(frappe._("Failed to connect to Muqeem Gateway: {0}").format(str(e)))
