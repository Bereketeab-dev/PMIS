import frappe
from frappe.model.document import Document

class DailyWorkPlanMaterial(Document):
    def validate(self):
        if self.item_code and not self.uom:
            self.uom = frappe.db.get_value("Item", self.item_code, "stock_uom")
        if self.item_code and not self.item_name:
            self.item_name = frappe.db.get_value("Item", self.item_code, "item_name")
