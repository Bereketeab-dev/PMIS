# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AsBuiltDrawing(Document):
    # autoname is set to format in JSON, so we don't need a custom autoname method here.

    def validate(self):
        if not self.drawing_title and self.drawing_number:
            self.drawing_title = f"As-Built: {self.drawing_number}"

        if self.status == "Approved" and not self.approval_date:
            self.approval_date = frappe.utils.nowdate()
            if not self.approved_by:
                self.approved_by = frappe.session.user # Default approver if not set

    # before_submit and on_submit can be used if there's a workflow involved.
    # For example, changing status from "Submitted for Review" to "Approved".
    pass
