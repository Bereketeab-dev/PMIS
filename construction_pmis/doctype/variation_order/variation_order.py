# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt

class VariationOrder(Document):
    def before_submit(self):
        self.status = "Pending Approval"
        if not self.description_of_change:
            frappe.throw("Detailed Description of Change is required before submitting.")
        if self.cost_impact_type != "No Change" and not self.estimated_cost_impact and not self.linked_cost_estimate:
            frappe.msgprint("Consider providing an Estimated Cost Impact or linking a detailed Cost Estimate.", indicator="orange", title="Cost Impact")
        if self.schedule_impact_type != "No Change" and not self.estimated_time_impact_days:
            frappe.msgprint("Consider providing an Estimated Time Impact in Days.", indicator="orange", title="Schedule Impact")


    def on_update_after_submit(self):
        # This method is called when a document (already submitted) is updated and saved.
        # For example, after approval fields are filled.
        self.update_project_impact()

    def on_submit(self):
        # This is called when the document transitions from Draft (0) to Submitted (1)
        pass # Handled by before_submit and workflow

    def on_cancel(self):
        self.status = "Cancelled"
        # Potentially reverse any financial or schedule impacts if already applied to project
        # This depends on how impacts are integrated.
        frappe.msgprint(f"Variation Order {self.name} has been cancelled.")
        self.update_project_impact(cancelled=True)

    def update_project_impact(self, cancelled=False):
        if self.project and self.status == "Approved": # Or "Implemented" based on workflow
            project = frappe.get_doc("Project", self.project)

            # Example: Update project's contract value or budget
            # This needs careful design: should it add to a specific field?
            # Does Project DocType have fields like 'total_approved_variations_cost'?
            # For now, this is a placeholder for more complex integration.

            # if hasattr(project, "update_project_ financials_due_to_vo"):
            #    project.update_project_financials_due_to_vo(self, cancelled)
            #    project.save(ignore_permissions=True)
            pass

    # Custom method for workflow action "Implement"
    def implement_variation(self):
        if self.status != "Approved":
            frappe.throw("Variation Order must be Approved before it can be Implemented.")

        self.db_set("status", "Implemented")
        # Logic to formally apply changes to project budget, schedule, etc.
        # This might involve creating Journal Entries, updating Project Tasks, etc.
        self.update_project_impact()
        frappe.msgprint(f"Variation Order {self.name} has been implemented.")

    # autoname is set in JSON as format:VO-{project}-{#####}
    pass
