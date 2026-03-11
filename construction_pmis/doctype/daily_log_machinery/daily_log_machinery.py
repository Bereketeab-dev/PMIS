import frappe
from frappe.model.document import Document

class DailyLogMachinery(Document):
    def validate(self):
        from frappe.utils import flt
        total_hours = flt(self.actual_running_hours) + flt(self.idle_hours) + flt(self.breakdown_hours)
        # Can add validation if total_hours exceeds 24 or typical shift, etc.
