# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, nowdate

class ProjectScheduleTask(Document):
    def validate(self):
        if self.start_date and self.end_date:
            if getdate(self.end_date) < getdate(self.start_date):
                frappe.throw(f"Planned End Date ({self.end_date}) cannot be before Planned Start Date ({self.start_date}) for task '{self.task_name}'.")
            self.duration = date_diff(getdate(self.end_date), getdate(self.start_date)) + 1
        else:
            self.duration = 0

        if self.actual_start_date and self.actual_end_date:
            if getdate(self.actual_end_date) < getdate(self.actual_start_date):
                frappe.throw(f"Actual End Date ({self.actual_end_date}) cannot be before Actual Start Date ({self.actual_start_date}) for task '{self.task_name}'.")

        if self.percent_complete == 100 and not self.actual_end_date:
            # frappe.msgprint(f"Task '{self.task_name}' is 100% complete. Consider setting the Actual End Date.", indicator="orange", title="Task Completion")
            self.actual_end_date = nowdate() # Default actual end date to today if 100%

        if self.status == "Completed" and self.percent_complete < 100:
            self.percent_complete = 100
            if not self.actual_end_date:
                 self.actual_end_date = nowdate()

        if self.status == "In Progress" and not self.actual_start_date:
            self.actual_start_date = nowdate()
            if self.percent_complete == 0:
                 self.percent_complete = 1 # Small progress when started

        # Update project's task HTML view after save
        if self.project:
            project_doc = frappe.get_doc("Project", self.project)
            if hasattr(project_doc, 'update_tasks_html'):
                project_doc.update_tasks_html()
                # Do not save project_doc here, it will be saved by the user or main transaction


    def on_update(self):
        # After this task is saved, if it's a predecessor to other tasks,
        # those tasks might need their schedule updated (if using auto-scheduling logic - not implemented here).
        pass

    # autoname is format:TASK-{project}-{#####} defined in JSON
pass


