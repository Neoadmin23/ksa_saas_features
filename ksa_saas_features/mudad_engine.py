import frappe
from frappe.utils import today, format_date

class MudadWPSEngine:
    """Generates standard Saudi WPS (Salary Information File - SIF) for Mudad."""

    def __init__(self, payroll_entry_id):
        self.payroll_entry = frappe.get_doc("Payroll Entry", payroll_entry_id)
        self.settings = frappe.get_single("SaaS Feature Settings")

    def generate_sif_content(self):
        est_id = self.settings.mudad_establishment_id or "7000000000"
        bank_code = self.settings.mudad_bank_code or "NCBK"
        employer_iban = self.settings.mudad_employer_iban or "SA0000000000000000000000"
        
        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={"payroll_entry": self.payroll_entry.name, "docstatus": 1},
            fields=["name", "employee", "employee_name", "net_pay", "gross_pay", "total_deduction", "bank_account_no", "bank_name"]
        )

        if not salary_slips:
            frappe.throw(frappe._("No submitted Salary Slips found for this Payroll Entry."))

        lines = []
        # Header Line: Record Type, Establishment ID, Bank Code, File Date, Time, Total Records, Total Amount
        total_amount = sum(float(slip.net_pay or 0.0) for slip in salary_slips)
        lines.append(f"SCR,EST,{est_id},{bank_code},{format_date(today(), 'YYYYMMDD')},{len(salary_slips)},{total_amount:.2f}")

        # Employee Record Lines
        for slip in salary_slips:
            emp = frappe.get_cached_value("Employee", slip.employee, ["bank_ac_no", "iban", "national_id_number", "iqama_number"], as_dict=True)
            national_id = emp.iqama_number or emp.national_id_number or "0000000000"
            iban = emp.iban or slip.bank_account_no or "SA0000000000000000000000"
            
            lines.append(
                f"EDR,EMP,{national_id},{iban},{slip.net_pay:.2f},{slip.gross_pay:.2f},{slip.total_deduction:.2f},0.00,{slip.employee_name}"
            )

        return "\n".join(lines)
