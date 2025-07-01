# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AsBuiltDrawing(Document):
    def autoname(self):
        # format:ABD-{project}-{drawing_number}
        # The drawing_number itself should be unique, so this might be redundant if drawing_number is set as title or unique.
        # However, this format ensures it's unique per project even if drawing numbers are not globally unique.
        # For autoname to use a field value, that field must be set before naming.
        # This is best handled by setting autoname to "Prompt" or "field:drawing_title" and ensuring drawing_number is unique.
        # If drawing_number is guaranteed unique, autoname = "field:drawing_number" is simplest.
        # Given current JSON autoname="format:ABD-{project}-{drawing_number}", this python method is not strictly needed
        # unless more complex series generation is required. Frappe will use the format string.
        pass

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
