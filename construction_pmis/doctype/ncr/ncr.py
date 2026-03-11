# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class NCR(Document):
    def autoname(self):
        # format:NCR-{project}-{YYYY}-{MM}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        year = getdate(self.date_raised).strftime("%Y") if self.date_raised else getdate(nowdate()).strftime("%Y")
        month = getdate(self.date_raised).strftime("%m") if self.date_raised else getdate(nowdate()).strftime("%m")
        prefix = f"NCR-{project_abbr}-{year}-{month}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if not self.subject:
            self.subject = f"{self.ncr_type or 'NCR'} - {self.project or 'General'} - {self.date_raised or nowdate()}"

        if self.status == "Closed" and not self.date_closed:
            self.date_closed = nowdate()
            if not self.closed_by:
                self.closed_by = frappe.session.user

        # If action is completed, but not yet verified
        if self.action_completion_date and self.status == "Corrective Action Implemented":
            self.status = "Pending Verification"


    def before_submit(self):
        # This might be called when transitioning from Draft to Open/Submitted
        if self.docstatus == 0: # Only on first submit
             if not self.status or self.status == "Draft": # Assuming workflow might set status first
                self.status = "Open"

    # Workflow actions can call specific methods
    def propose_corrective_action(self):
        if not self.proposed_corrective_action or not self.action_assigned_to:
            frappe.throw("Please provide Proposed Corrective Action and Assign To before proceeding.")
        self.db_set("status", "Corrective Action Proposed")

    def implement_corrective_action(self):
        if not self.action_taken_details or not self.action_completion_date:
            frappe.throw("Please provide Details of Action Taken and Actual Completion Date.")
        self.db_set("status", "Corrective Action Implemented")

    def verify_and_close_ncr(self):
        if not self.verification_by or not self.verification_date or not self.verification_remarks:
            frappe.throw("Verification details (Verified By, Date, Remarks) are required for closure.")

        # Add logic here to check if action was effective.
        # For example, a checkbox "Action Effective?" could be added.
        # if not self.action_effective: # Assuming a field `action_effective` (Check type)
        #    frappe.throw("Corrective action must be verified as effective before closing.")

        self.db_set("status", "Closed")
        self.db_set("closed_by", frappe.session.user)
        self.db_set("date_closed", nowdate())
        frappe.msgprint(f"NCR {self.name} has been verified and closed.")

    def reject_ncr(self):
        # This might be an early rejection if NCR is deemed invalid
        self.db_set("status", "Rejected")
        frappe.msgprint(f"NCR {self.name} has been rejected.")

pass
