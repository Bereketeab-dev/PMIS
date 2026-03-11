import frappe
from frappe.model.document import Document
from frappe.utils import flt

class SubcontractItem(Document):
    def validate(self):
        self.calculate_amount()
        self.trigger_parent_recalculation()

    def calculate_amount(self):
        self.amount = flt(self.quantity) * flt(self.unit_rate)

    def trigger_parent_recalculation(self):
        if self.parenttype == "Subcontract" and self.parent:
            parent_doc = frappe.get_doc(self.parenttype, self.parent)
            if hasattr(parent_doc, 'calculate_total_subcontract_value'):
                parent_doc.calculate_total_subcontract_value()
