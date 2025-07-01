# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, date_diff, getdate

class ManpowerPlanItem(Document):
    def validate(self):
        self.calculate_durations()

    def calculate_durations(self):
        if self.start_date and self.end_date:
            self.planned_total_days = date_diff(getdate(self.end_date), getdate(self.start_date)) + 1
            if self.planned_total_days < 0:
                frappe.throw(f"Row {self.idx}: End Date cannot be before Start Date for Manpower Plan.")
        else:
            self.planned_total_days = 0

        self.total_planned_hours = flt(self.planned_total_days) * flt(self.planned_hours_per_day) * flt(self.required_quantity)

    # autoname can be set if needed for child table uniqueness if ever detached or directly queried.
    # def autoname(self):
    #     if self.parent and self.resource_type:
    #         self.name = f"{self.parent}-MPI-{frappe.utils.slug(self.resource_type)}-{self.idx}"
    #     else:
    #         pass # Default naming for child table
pass
