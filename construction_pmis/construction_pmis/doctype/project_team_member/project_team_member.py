# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProjectTeamMember(Document):
    def autoname(self):
        # Autoname for child table records is typically handled by the parent DocType
        # or can be based on a hash of values if global uniqueness is needed (rare for child tables).
        # For simplicity, we can use 'Prompt' in JSON which means user has to provide name, or it's set by parent.
        # Or, we can construct a name if needed, though often it's just `parent_name_row_index`.
        if self.user and self.parent: # self.parent would be the Project name
             self.name = f"{self.parent}-{self.user}-{self.idx}" # Example: ProjectName-UserName-1
        else:
             # Fallback if fields not set, though parent and idx are usually available
             # This will likely be overridden by Frappe's default child naming if autoname is "Prompt" or similar
             # For child tables, name is not that critical as they are accessed via parent.
             pass

    def validate(self):
        # Fetch user details if not provided
        if self.user and not (self.contact_number and self.email_id):
            user_doc = frappe.get_doc("User", self.user)
            if not self.contact_number and user_doc.phone:
                self.contact_number = user_doc.phone
            if not self.email_id: # Always fetch email from user doc as primary
                self.email_id = user_doc.email
pass
