# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class SiteInspection(Document):
    def autoname(self):
        # format:INSP-{project}-{date}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        current_date_str = getdate(self.inspection_date).strftime("%Y%m%d") if self.inspection_date else nowdate().replace("-","")
        self.name = f"INSP-{project_abbr}-{current_date_str}-"

    def validate(self):
        if not self.inspection_title:
            self.inspection_title = f"{self.inspection_type} for {self.project} on {self.inspection_date}"

    def before_submit(self):
        self.status = "Pending Review" # Or as per workflow

    def on_submit(self):
        # Logic after submission, e.g., if status needs to be updated based on findings
        # Or notify relevant parties
        pass

    @frappe.whitelist()
    def populate_checklist_from_template(self):
        if not self.checklist_template:
            frappe.throw("Please select a Checklist Template first.")
            return

        template = frappe.get_doc("Site Inspection Checklist Template", self.checklist_template)
        self.set("checklist_items", []) # Clear existing items

        for item in template.checklist_template_items:
            self.append("checklist_items", {
                "template_item_ref": item.name,
                "sequence_id": item.sequence_id,
                "checkpoint_description": item.checkpoint_description,
                "expected_outcome_criteria": item.expected_outcome_criteria,
                "observation_status": "N/A" # Default status, user to fill
            })
        frappe.msgprint("Checklist items populated from template. Please fill in observations.")

