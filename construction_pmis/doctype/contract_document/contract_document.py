# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ContractDocument(Document):
    def validate(self):
        if self.effective_date and self.expiry_date and self.expiry_date < self.effective_date:
            frappe.throw("Expiry Date cannot be before Effective Date.")

        # Call update_project_links after save, because self.name needs to be set for the link to be correct
        # This is better done in an on_update or after_save hook if possible,
        # but for direct feedback in UI, sometimes validate is used.
        # However, for updating another doctype (Project), it's best done after this document is saved.

    def on_update(self):
        # Update the HTML field in the linked Project
        if self.project:
            project_doc = frappe.get_doc("Project", self.project)
            project_doc.update_links_html() # Assuming this method exists in Project.py
            project_doc.save(ignore_permissions=True) # Save the project document

    def on_trash(self):
        # When a contract document is deleted, update the project's HTML field
        if self.project:
            project_doc = frappe.get_doc("Project", self.project)
            project_doc.update_links_html()
            project_doc.save(ignore_permissions=True)

# Child DocType: Contract Document Link (for linking related documents)
# This will be a separate DocType definition.
pass
