import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class CommissioningChecklistItem(Document):
    def validate(self):
        if self.result_status in ["Pass", "Fail", "N/A"] and not self.verification_date:
            self.verification_date = nowdate()
            if not self.verified_by:
                self.verified_by = frappe.session.user # Default verifier
