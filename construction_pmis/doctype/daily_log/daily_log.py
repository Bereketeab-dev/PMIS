# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, flt

class DailyLog(Document):
    def autoname(self):
        # format:DL-{project}-{date}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        current_date_str = getdate(self.date).strftime("%Y%m%d") if self.date else nowdate().replace("-","")
        prefix = f"DL-{project_abbr}-{current_date_str}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if not self.log_title:
            self.log_title = f"Daily Log for {self.project} on {self.date}"

        # Update task statuses in Project Schedule Task based on Daily Log Task Progress
        for progress_item in self.tasks_progress:
            if progress_item.project_schedule_task and progress_item.status:
                # Update the main Project Schedule Task
                # Consider if this update should only happen on submit/approval of Daily Log
                frappe.db.set_value("Project Schedule Task",
                                    progress_item.project_schedule_task,
                                    "status",
                                    progress_item.status,
                                    update_modified=False) # Avoid recursion if PST validate triggers project save
                if progress_item.cumulative_percent_complete is not None:
                     frappe.db.set_value("Project Schedule Task",
                                    progress_item.project_schedule_task,
                                    "percent_complete",
                                    progress_item.cumulative_percent_complete,
                                    update_modified=False)


    def before_submit(self):
        self.status = "Submitted"
        # Could add validation: e.g., at least one work progress item, or actual manpower recorded.

    def on_submit(self):
        # After submit, could trigger:
        # - Update actual costs on project (if manpower/machinery hours translate to cost)
        # - Update inventory for materials consumed (create Stock Entry)
        # - Update Project Schedule Task actual start/end dates based on progress.
        self.update_project_schedule_tasks_from_log()


    def on_update_after_submit(self):
        # If an approved log is amended and saved.
        self.update_project_schedule_tasks_from_log()


    def update_project_schedule_tasks_from_log(self):
        for prog_item in self.get("tasks_progress"):
            if prog_item.project_schedule_task:
                task_doc = frappe.get_doc("Project Schedule Task", prog_item.project_schedule_task)

                # Update status
                if prog_item.status and task_doc.status != prog_item.status:
                    task_doc.status = prog_item.status

                # Update % complete
                if prog_item.cumulative_percent_complete is not None and task_doc.percent_complete != prog_item.cumulative_percent_complete :
                    task_doc.percent_complete = prog_item.cumulative_percent_complete

                # Update actual start date
                if prog_item.status in ["In Progress", "Partially Completed", "Completed"] and not task_doc.actual_start_date:
                    task_doc.actual_start_date = self.date

                # Update actual end date
                if prog_item.status == "Completed" and not task_doc.actual_end_date:
                    task_doc.actual_end_date = self.date

                if task_doc.is_dirty():
                    task_doc.save(ignore_permissions=True) # Save changes to the task


    @frappe.whitelist()
    def populate_from_daily_work_plan(self):
        if not self.linked_daily_work_plan:
            frappe.throw("Please link a Daily Work Plan first.")
            return

        dwp = frappe.get_doc("Daily Work Plan", self.linked_daily_work_plan)
        if dwp.project != self.project or getdate(dwp.date) != getdate(self.date):
            frappe.throw("Linked Daily Work Plan project or date does not match this Daily Log.")

        # Populate Tasks Progress
        self.set("tasks_progress", [])
        for dwp_task in dwp.planned_tasks_for_day:
            self.append("tasks_progress", {
                "daily_work_plan_task": dwp_task.name,
                "project_schedule_task": dwp_task.project_schedule_task,
                "task_name": dwp_task.task_name,
                "unit_of_measure": dwp_task.unit_of_measure,
                "status": "Not Started" # Default status
            })

        # Populate Actual Manpower
        self.set("manpower_actual", [])
        for dwp_manpower in dwp.planned_manpower:
            self.append("manpower_actual", {
                "daily_work_plan_manpower": dwp_manpower.name,
                "resource_type": dwp_manpower.resource_type,
                "specific_employee": dwp_manpower.specific_employee,
                "actual_quantity": dwp_manpower.planned_quantity,
                "actual_hours_worked": dwp_manpower.planned_hours
            })

        # Populate Actual Machinery
        self.set("machinery_actual", [])
        for dwp_machinery in dwp.planned_machinery:
            self.append("machinery_actual", {
                "daily_work_plan_machinery": dwp_machinery.name,
                "machinery_asset": dwp_machinery.machinery_asset,
                "machinery_type": dwp_machinery.machinery_type,
                "actual_quantity": dwp_machinery.planned_quantity,
                "actual_running_hours": dwp_machinery.planned_hours,
                "operator_name": dwp_machinery.operator_name
            })

        # Populate Actual Materials (as 'Consumed' by default)
        self.set("materials_consumed_actual", [])
        for dwp_material in dwp.planned_materials:
            self.append("materials_consumed_actual", {
                "daily_work_plan_material": dwp_material.name,
                "item_code": dwp_material.item_code,
                "item_name": dwp_material.item_name,
                "transaction_type": "Consumed",
                "quantity": dwp_material.required_quantity,
                "uom": dwp_material.uom,
                "source_or_target_warehouse": dwp_material.source_warehouse
            })

        self.work_completed_today = f"Activities based on Daily Work Plan: {self.linked_daily_work_plan}.\n" + (dwp.specific_instructions or "")
        # self.toolbox_talk_conducted = dwp.safety_precautions # safety_precautions is likely Text, toolbox_talk_conducted is Link

        frappe.msgprint("Data populated from linked Daily Work Plan. Please verify and fill actuals.")


