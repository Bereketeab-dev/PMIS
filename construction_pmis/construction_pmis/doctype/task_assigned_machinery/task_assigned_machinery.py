# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TaskAssignedMachinery(Document):
    def validate(self):
        if not self.machinery_plan_item and not self.machinery_asset and not self.machinery_type:
            frappe.throw(f"Row {self.idx}: Either select Machinery from Project Plan, a specific Asset, or specify Machinery Type.")

        if self.machinery_plan_item:
            plan_item = frappe.get_doc("Machinery Plan Item", self.machinery_plan_item)
            self.machinery_asset = plan_item.machinery_asset
            self.machinery_type = plan_item.machinery_type
            # self.quantity = plan_item.required_quantity # Or check if assigned qty exceeds planned
        elif self.machinery_asset and not self.machinery_type:
            # Fetch machinery_type from Asset if only asset is provided
            asset_doc = frappe.get_doc("Asset", self.machinery_asset)
            self.machinery_type = asset_doc.get("asset_name") # or asset_doc.asset_category

        if not self.quantity or self.quantity <= 0:
            self.quantity = 1
pass

# Corresponding get_query function in utils.py:
# @frappe.whitelist()
# def get_machinery_plan_items_for_project(doctype, txt, searchfield, start, page_len, filters):
#     project_name = filters.get("project")
#     if not project_name:
#         if filters.get("parent_doctype") == "Project Schedule Task" and filters.get("parent_docname"):
#             project_name = frappe.db.get_value(filters.get("parent_doctype"), filters.get("parent_docname"), "project")
#
#     if not project_name:
#         return []
#
#     # This assumes Machinery Plan Item is a child table of Project.
#     return frappe.db.sql(f"""
#         SELECT mpi.name, mpi.machinery_type, asset.asset_name
#         FROM `tabMachinery Plan Item` mpi
#         LEFT JOIN `tabAsset` asset ON mpi.machinery_asset = asset.name
#         WHERE mpi.parent = %(project_name)s
#         AND mpi.docstatus = 0
#         AND (mpi.machinery_type LIKE %(txt)s OR asset.asset_name LIKE %(txt)s OR mpi.name LIKE %(txt)s)
#         ORDER BY mpi.machinery_type
#         LIMIT %(start)s, %(page_len)s
#     """, {
#         "project_name": project_name,
#         "txt": "%%%s%%" % txt,
#         "start": start,
#         "page_len": page_len
#     }, as_list=True)
