import frappe
from frappe.model.document import Document

class ToolboxTalkAttendee(Document):
    def validate(self):
        if self.employee and not self.attendee_name:
            self.attendee_name = frappe.get_cached_value("Employee", self.employee, "employee_name")
        if self.employee and not self.company_contractor:
            self.company_contractor = frappe.get_cached_value("Employee", self.employee, "company")
