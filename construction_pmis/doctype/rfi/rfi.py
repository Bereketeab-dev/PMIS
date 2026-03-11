# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class RFI(Document):
    def before_submit(self):
        if not self.assigned_to:
            frappe.throw("Please assign the RFI to a user before submitting.")
        self.status = "Submitted"

    def on_update_after_submit(self):
        # This is called when the document is updated *after* it has been submitted.
        # Useful for when a response is added.
        if self.response and not self.date_responded:
            self.db_set("date_responded", now_datetime())
            self.db_set("responded_by", frappe.session.user)
            self.db_set("status", "Responded") # Or as per workflow transition

        # If workflow handles status changes, this might not be needed or could conflict.
        # Ensure workflow transitions correctly update the status field.

    # Example: A custom method that might be called by a workflow action
    def close_rfi(self):
        self.db_set("status", "Closed")
        frappe.msgprint(f"RFI {self.name} has been closed.")

    def reopen_rfi(self):
        # Check if user has permission to reopen, or if RFI is in a state that allows reopening.
        if self.status not in ["Closed", "Void"]: # Example condition
             frappe.throw("RFI cannot be reopened from its current state.")
        self.db_set("status", "Open") # Or 'Under Review' depending on process
        # Clear response fields if needed
        # self.db_set("response", None)
        # self.db_set("date_responded", None)
        # self.db_set("responded_by", None)
        frappe.msgprint(f"RFI {self.name} has been reopened.")

    # autoname is set in JSON as format:RFI-{project}-{#####}
    pass
