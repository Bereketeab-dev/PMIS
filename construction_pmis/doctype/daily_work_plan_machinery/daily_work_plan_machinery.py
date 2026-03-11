import frappe
from frappe.model.document import Document

class DailyWorkPlanMachinery(Document):
    def validate(self):
        if self.machinery_plan_item:
            details = frappe.get_doc("Machinery Plan Item", self.machinery_plan_item)
            self.machinery_asset = details.machinery_asset
            self.machinery_type = details.machinery_type
        elif not self.machinery_type and not self.machinery_asset:
             frappe.throw("Machinery Type or Specific Asset is required if not linking from Project Machinery Plan.")
        elif self.machinery_asset and not self.machinery_type:
            self.machinery_type = frappe.db.get_value("Asset", self.machinery_asset, "asset_name")
