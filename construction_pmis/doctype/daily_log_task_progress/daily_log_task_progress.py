import frappe
from frappe.model.document import Document

class DailyLogTaskProgress(Document):
    def validate(self):
        from frappe.utils import flt
        if self.daily_work_plan_task and not self.task_name:
            # Fetch if not auto-fetched
            dwp_task_name = frappe.get_cached_value("Daily Work Plan Task", self.daily_work_plan_task, "task_name")
            self.task_name = dwp_task_name

        if self.daily_work_plan_task and not self.project_schedule_task:
            self.project_schedule_task = frappe.get_cached_value("Daily Work Plan Task", self.daily_work_plan_task, "project_schedule_task")

        if self.percent_complete_today is not None and (flt(self.percent_complete_today) < 0 or flt(self.percent_complete_today) > 100):
            frappe.throw(f"Row {self.idx}: Percent Complete Today must be between 0 and 100.")

        if self.cumulative_percent_complete is not None and (flt(self.cumulative_percent_complete) < 0 or flt(self.cumulative_percent_complete) > 100):
            frappe.throw(f"Row {self.idx}: Cumulative Percent Complete must be between 0 and 100.")

        if self.status == "Completed" and self.cumulative_percent_complete != 100:
            self.cumulative_percent_complete = 100 # Auto-set if status is completed
