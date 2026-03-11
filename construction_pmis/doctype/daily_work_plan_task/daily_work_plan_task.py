import frappe
from frappe.model.document import Document

class DailyWorkPlanTask(Document):
    def validate(self):
        if self.project_schedule_task and not self.task_name:
            self.task_name = frappe.db.get_value("Project Schedule Task", self.project_schedule_task, "task_name")
        if self.planned_start_time and self.planned_end_time and self.planned_end_time < self.planned_start_time:
            frappe.throw(f"For task '{self.task_name}', Planned End Time cannot be before Planned Start Time.")
