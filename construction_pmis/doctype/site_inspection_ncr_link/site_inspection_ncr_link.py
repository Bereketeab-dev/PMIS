import frappe
from frappe.model.document import Document

class SiteInspectionNCRLink(Document):
    def validate(self):
        if self.ncr:
            ncr_doc = frappe.get_doc("NCR", self.ncr)
            self.ncr_status = ncr_doc.status
            self.ncr_description = ncr_doc.subject # Assuming NCR has a 'subject' field for title/short desc
