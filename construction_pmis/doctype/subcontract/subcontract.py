# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate

class Subcontract(Document):
    def autoname(self):
        # format:SUB-{project}-{supplier_abbr}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        supplier_abbr = ""
        if self.supplier:
            supplier_name = frappe.get_cached_value('Supplier', self.supplier, 'supplier_name')
            # Create abbreviation from supplier name, e.g., first 3-5 chars or initials
            parts = supplier_name.split()
            if len(parts) > 1:
                supplier_abbr = "".join(part[0] for part in parts[:2]).upper() # First letter of first two words
            else:
                supplier_abbr = supplier_name[:3].upper()

        prefix = f"SUB-{project_abbr}-{supplier_abbr}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")


    def validate(self):
        self.calculate_total_subcontract_value()
        if self.commencement_date and self.completion_date and getdate(self.completion_date) < getdate(self.commencement_date):
            frappe.throw("Planned Completion Date cannot be before Planned Commencement Date.")

    def calculate_total_subcontract_value(self):
        total_value = 0
        if self.subcontract_items:
            for item in self.subcontract_items:
                item.amount = flt(item.quantity) * flt(item.unit_rate) # Ensure child item amount is calculated
                total_value += flt(item.amount)
        self.subcontract_value = total_value

    def before_submit(self):
        self.status = "Pending Award" # Or directly to "Awarded" if no separate award step in workflow

    def on_submit(self): # Or a custom workflow action like "Award Subcontract"
        self.status = "Awarded" # Or "Active"
        # Potentially create a Purchase Order if integration is desired and not manually linked
        # self.create_purchase_order_for_subcontract()

    def on_cancel(self):
        self.status = "Cancelled"
        # If a PO was created, it might need to be cancelled too.
        # if self.linked_purchase_order:
        #     po = frappe.get_doc("Purchase Order", self.linked_purchase_order)
        #     if po.docstatus == 1: # Submitted PO
        #         po.cancel()
        #         frappe.msgprint(f"Linked Purchase Order {self.linked_purchase_order} cancelled.")
        #     self.db_set("linked_purchase_order", None)

    # Example method to be called by workflow
    def award_subcontract(self):
        if self.status not in ["Draft", "Pending Award"]:
             frappe.throw("Subcontract can only be awarded from Draft or Pending Award state.")
        self.status = "Awarded"
        self.db_set("status", "Awarded")
        # Any other logic on award, e.g., notifications
        frappe.msgprint(f"Subcontract {self.name} has been awarded to {self.supplier}.")
