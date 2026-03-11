# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class DailyWorkPlan(Document):
    def autoname(self):
        # format:DWP-{project}-{date}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        current_date_str = getdate(self.date).strftime("%Y%m%d") if self.date else nowdate().replace("-","")
        self.name = f"DWP-{project_abbr}-{current_date_str}-"

    def validate(self):
        if not self.plan_title:
            self.plan_title = f"Daily Plan for {self.project} on {self.date}"

    @frappe.whitelist()
    def get_tasks_for_day(self):
        if not self.project or not self.date:
            frappe.throw("Please select Project and Date first to fetch tasks.")

        self.set("planned_tasks_for_day", []) # Clear existing tasks

        # Fetch tasks from Project Schedule Task that are active for this day
        # Active means: planned_start_date <= self.date AND planned_end_date >= self.date
        # And status is not 'Completed' or 'Cancelled'
        tasks = frappe.get_all("Project Schedule Task",
            filters={
                "project": self.project,
                "start_date": ["<=", self.date],
                "end_date": [">=", self.date],
                "status": ["not in", ["Completed", "Cancelled"]]
            },
            fields=["name", "task_name", "wbs_reference", "start_date", "end_date"]
        )

        for task in tasks:
            self.append("planned_tasks_for_day", {
                "project_schedule_task": task.name,
                "task_name": task.task_name,
                "wbs_reference": task.wbs_reference
                # User can fill in time, location, target qty
            })

        # Also fetch planned manpower and machinery based on project plan for this date
        self.get_resources_for_day()


    @frappe.whitelist()
    def get_resources_for_day(self):
        if not self.project or not self.date:
            # This might be called after tasks are fetched, so project/date should be there
            # frappe.throw("Please select Project and Date first to fetch resources.")
            return

        self.set("planned_manpower", [])
        self.set("planned_machinery", [])

        # Fetch Manpower from Project's Manpower Plan active for this date
        manpower_plans = frappe.get_all("Manpower Plan Item",
            filters={
                "parent": self.project, # parent is the Project doc
                "parenttype": "Project",
                "start_date": ["<=", self.date],
                "end_date": [">=", self.date],
                "docstatus":0 # only from saved project
            },
            fields=["name", "resource_type", "employee", "required_quantity", "planned_hours_per_day"]
        )
        for mp in manpower_plans:
            self.append("planned_manpower", {
                "manpower_plan_item": mp.name,
                "resource_type": mp.resource_type,
                "specific_employee": mp.employee,
                "planned_quantity": mp.required_quantity,
                "planned_hours": mp.planned_hours_per_day
            })

        # Fetch Machinery from Project's Machinery Plan active for this date
        machinery_plans = frappe.get_all("Machinery Plan Item",
            filters={
                "parent": self.project, # parent is the Project doc
                "parenttype": "Project",
                "start_date": ["<=", self.date],
                "end_date": [">=", self.date],
                "docstatus":0
            },
            fields=["name", "machinery_asset", "machinery_type", "required_quantity", "planned_hours_per_day"]
        )
        for mchp in machinery_plans:
            self.append("planned_machinery", {
                "machinery_plan_item": mchp.name,
                "machinery_asset": mchp.machinery_asset,
                "machinery_type": mchp.machinery_type,
                "planned_quantity": mchp.required_quantity,
                "planned_hours": mchp.planned_hours_per_day
            })

    # After submit, this plan might become read-only or trigger notifications.
    # Workflow can handle status changes.
pass


# Child DocType python files (minimal, as logic is mostly in JSON or parent)

class DailyWorkPlanTask(Document):
    def validate(self):
        if self.project_schedule_task and not self.task_name:
            self.task_name = frappe.db.get_value("Project Schedule Task", self.project_schedule_task, "task_name")
        if self.planned_start_time and self.planned_end_time and self.planned_end_time < self.planned_start_time:
            frappe.throw(f"For task '{self.task_name}', Planned End Time cannot be before Planned Start Time.")
    pass

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
    pass

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

    pass

class DailyWorkPlanMaterial(Document):
    def validate(self):
        if self.item_code and not self.uom:
            self.uom = frappe.db.get_value("Item", self.item_code, "stock_uom")
        if self.item_code and not self.item_name:
            self.item_name = frappe.db.get_value("Item", self.item_code, "item_name")

    pass
