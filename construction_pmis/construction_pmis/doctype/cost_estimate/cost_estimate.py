# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class CostEstimate(Document):
    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        total_boq_amount = 0
        if self.boq_items:
            for item in self.boq_items:
                total_boq_amount += flt(item.amount)
        self.total_boq_amount = total_boq_amount

        contingency_amount = (flt(self.total_boq_amount) * flt(self.contingency_percentage)) / 100
        self.contingency_amount = contingency_amount

        self.total_estimated_amount = flt(self.total_boq_amount) + flt(self.contingency_amount)

    # After submit, update the Project's total estimated cost
    def on_submit(self):
        if self.project:
            try:
                project_doc = frappe.get_doc("Project", self.project)
                # This is a simplified update; a more robust solution might sum up all approved estimates
                # or have a specific field on Project for the "active" or "latest approved" estimate.
                # For now, let's assume this estimate's amount should be reflected.
                # project_doc.total_estimated_cost = self.total_estimated_amount # This might overwrite other estimates
                # project_doc.save(ignore_permissions=True)

                # A better approach: sum up all 'Approved' and 'Submitted' (if applicable) cost estimates for the project
                # This requires a method on the Project DocType.
                if hasattr(project_doc, 'update_total_estimated_cost'):
                    project_doc.update_total_estimated_cost() # Call method on Project to recalculate
                    project_doc.save(ignore_permissions=True)
                else:
                    # Fallback if method doesn't exist: simple update (less ideal)
                    # This could be dangerous if there are multiple estimates.
                    # frappe.db.set_value("Project", self.project, "total_estimated_cost", self.total_estimated_amount)
                    pass # Decide on a strategy: for now, let project handle its sum.

            except frappe.DoesNotExistError:
                frappe.log_error(f"Project {self.project} not found for Cost Estimate {self.name}", "Cost Estimate Linking Error")


    def on_cancel(self):
        # If a cost estimate is cancelled, the project's total estimated cost might need recalculation.
        if self.project:
            try:
                project_doc = frappe.get_doc("Project", self.project)
                if hasattr(project_doc, 'update_total_estimated_cost'):
                    project_doc.update_total_estimated_cost()
                    project_doc.save(ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass # Project might not exist or already deleted.

# Child DocType: Bill of Quantities Item
# This will be a separate DocType definition.
pass
