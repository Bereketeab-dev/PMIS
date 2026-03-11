# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TaskAssignedManpower(Document):
    def validate(self):
        if not self.manpower_plan_item and not self.resource_type:
            frappe.throw(f"Row {self.idx}: Either select Manpower from Project Plan or specify Resource Type.")

        if self.manpower_plan_item:
            # Fetch latest details if they might change and aren't auto-fetched by framework
            # For example, if resource_type on ManpowerPlanItem could change after linking.
            # However, 'fetch_from' usually handles initial data population.
            # This is more for ensuring data consistency if linked source can change.
            plan_item = frappe.get_doc("Manpower Plan Item", self.manpower_plan_item)
            self.resource_type = plan_item.resource_type
            self.specific_employee = plan_item.employee
            # Decide if quantity should be capped by plan_item.required_quantity
            # if self.quantity > plan_item.required_quantity:
            #     self.quantity = plan_item.required_quantity # Or throw error/warning
            pass

        if not self.quantity or self.quantity <= 0:
            self.quantity = 1 # Default to 1 if not set or invalid
pass

# Utility function for get_query in JSON (needs to be in a .py file accessible by hooks)
# This function would typically reside in project_schedule_task.py or a general utils.py for the app.
# For now, I will create a utils.py for such queries.
# Path: construction_pmis/construction_pmis/utils.py
# Content:
# import frappe
# @frappe.whitelist()
# def get_manpower_plan_items_for_project(doctype, txt, searchfield, start, page_len, filters):
#     project_name = filters.get("project") # Assuming parent ProjectScheduleTask has project field
#     if not project_name:
#         # Try to get project from the parent document if this is being called from within a Task form
#         if filters.get("parent_doctype") == "Project Schedule Task" and filters.get("parent_docname"):
#             project_name = frappe.db.get_value(filters.get("parent_doctype"), filters.get("parent_docname"), "project")
#
#     if not project_name:
#         return [] # Or raise error, or return all if that's desired behavior
#
#     # Find the Manpower Plan Items linked to the Project (which is the grandparent of this child table row)
#     # This assumes Manpower Plan Item is a child table of Project.
#     # The actual Manpower Plan Item name is usually like ProjectName-MPI-Resource-IDX
#     # We need to query Manpower Plan Item where parent = project_name
#
#     return frappe.db.sql(f"""
#         SELECT name, resource_type, required_quantity
#         FROM `tabManpower Plan Item`
#         WHERE parent = %(project_name)s
#         AND docstatus = 0
#         AND (resource_type LIKE %(txt)s OR name LIKE %(txt)s)
#         ORDER BY resource_type
#         LIMIT %(start)s, %(page_len)s
#     """, {
#         "project_name": project_name,
#         "txt": "%%%s%%" % txt,
#         "start": start,
#         "page_len": page_len
#     }, as_list=True)

# The above utility function needs to be created.
# I will create `construction_pmis/construction_pmis/utils.py` next.
