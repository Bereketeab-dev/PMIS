# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, date_diff, getdate

class MachineryPlanItem(Document):
    def validate(self):
        self.calculate_durations()
        if self.machinery_asset and not self.machinery_type:
            # Attempt to fetch machinery_type from Asset's item_group or a custom field if it exists
            asset_doc = frappe.get_doc("Asset", self.machinery_asset)
            self.machinery_type = asset_doc.get("asset_name") # or asset_doc.item_code or asset_doc.asset_category

    def calculate_durations(self):
        if self.start_date and self.end_date:
            self.planned_total_days = date_diff(getdate(self.end_date), getdate(self.start_date)) + 1
            if self.planned_total_days < 0:
                 frappe.throw(f"Row {self.idx}: End Date cannot be before Start Date for Machinery Plan.")
        else:
            self.planned_total_days = 0

        self.total_planned_hours = flt(self.planned_total_days) * flt(self.planned_hours_per_day) * flt(self.required_quantity)

    # autoname for child table
    # def autoname(self):
    #     if self.parent and self.machinery_asset:
    #         asset_name_slug = frappe.utils.slug(frappe.db.get_value("Asset", self.machinery_asset, "asset_name") or self.machinery_type or "machine")
    #         self.name = f"{self.parent}-MCH-{asset_name_slug}-{self.idx}"
    #     else:
    #         pass
pass
