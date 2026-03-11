# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class SnagListItem(Document):
    def autoname(self):
        # format:SNAG-{project}-{YYYY}-{MM}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        year = getdate(self.date_identified).strftime("%Y") if self.date_identified else getdate(nowdate()).strftime("%Y")
        month = getdate(self.date_identified).strftime("%m") if self.date_identified else getdate(nowdate()).strftime("%m")
        prefix = f"SNAG-{project_abbr}-{year}-{month}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if self.status == "Closed" and not self.date_closed:
            self.date_closed = nowdate()

        if self.status == "Rectified" and not self.date_rectified:
            self.date_rectified = nowdate()
            # Consider changing status to "Pending Re-inspection" if a re-inspection step is formal
            # self.status = "Pending Re-inspection"

        if self.re_inspection_status == "Approved" and self.status != "Closed":
            self.status = "Closed"
            if not self.date_closed:
                 self.date_closed = nowdate()
        elif self.re_inspection_status == "Rejected" and self.status == "Pending Re-inspection":
            self.status = "Work In Progress" # Or back to "Assigned" or "Open"
            frappe.msgprint("Re-inspection rejected. Snag requires further action.", indicator="orange")


    def before_submit(self):
        # Snag List Items might not always need a formal submit (docstatus=1) like transactional docs.
        # Workflow can manage state changes. If submitted, status could change from Draft to Open.
        if self.docstatus == 0 and self.status == "Draft": # Assuming "Draft" is a custom pre-open state not in workflow
            self.status = "Open"

    # Workflow methods
    def assign_for_rectification(self):
        if not self.assigned_to_party and not self.assigned_to_user:
            frappe.throw("Please assign the snag to a Party or User for rectification.")
        if not self.target_rectification_date:
            frappe.msgprint("Consider setting a Target Rectification Date.", indicator="orange")
        self.db_set("status", "Assigned")

    def start_rectification_work(self):
        self.db_set("status", "Work In Progress")

    def mark_as_rectified(self):
        if not self.rectification_action_taken or not self.date_rectified:
            frappe.throw("Please provide Rectification Action Taken details and Date Rectified.")
        self.db_set("status", "Rectified") # Or "Pending Re-inspection" if that's a distinct step

    def re_inspect_and_close(self):
        if self.re_inspection_status == "Approved":
            self.db_set("status", "Closed")
            self.db_set("date_closed", self.re_inspection_date or nowdate())
            frappe.msgprint(f"Snag {self.name} re-inspected and closed.")
        elif self.re_inspection_status == "Rejected":
            self.db_set("status", "Work In Progress") # Or "Assigned"
            frappe.msgprint(f"Snag {self.name} re-inspection rejected. Further action needed.", indicator="orange")
        else:
            frappe.throw("Please set Re-inspection Status (Approved/Rejected).")

    def reject_snag(self):
        # If a snag is deemed invalid after identification
        self.db_set("status", "Rejected")
        frappe.msgprint(f"Snag {self.name} has been rejected/marked as invalid.")

pass
