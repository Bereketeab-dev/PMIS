import frappe
from frappe.model.document import Document

class DailyWorkPlanManpower(Document):
    def validate(self):
        if self.manpower_plan_item:
            # Fetch if not auto-fetched (though 'fetch_from' should work)
            details = frappe.get_doc("Manpower Plan Item", self.manpower_plan_item)
            self.resource_type = details.resource_type
            self.specific_employee = details.employee
            # self.planned_quantity = details.required_quantity # Or allow override
            # self.planned_hours = details.planned_hours_per_day
        elif not self.resource_type:
            frappe.throw("Resource Type is required if not linking from Project Manpower Plan.")
