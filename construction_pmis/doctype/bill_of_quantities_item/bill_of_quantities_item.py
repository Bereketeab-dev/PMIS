import frappe
from frappe.model.document import Document
from frappe.utils import flt

class BillofQuantitiesItem(Document):
    def validate(self):
        self.calculate_amount()

    def calculate_amount(self):
        self.amount = flt(self.quantity) * flt(self.unit_rate)
