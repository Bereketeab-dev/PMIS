# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProjectStakeholder(Document):
    def autoname(self):
        if self.stakeholder_name and self.parent:
            self.name = f"{self.parent}-{self.stakeholder_type}-{self.stakeholder_name[:20].strip().replace(' ','-')}-{self.idx}"
        else:
            pass

    def validate(self):
        if self.supplier:
            supplier_doc = frappe.get_doc("Supplier", self.supplier)
            if not self.stakeholder_name:
                self.stakeholder_name = supplier_doc.supplier_name
            if not self.company_name and supplier_doc.company_name:
                self.company_name = supplier_doc.company_name
            # You might want to fetch primary contact details from Supplier's contacts
            # For simplicity, this is not implemented here.
pass
