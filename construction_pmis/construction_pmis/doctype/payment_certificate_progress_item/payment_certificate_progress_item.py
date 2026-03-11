# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class PaymentCertificateProgressItem(Document):
    def validate(self):
        self.update_calculations()
        self.trigger_parent_calculation()

    def on_change(self): # Primarily for client-side, server equivalent is validate
        self.update_calculations()
        # self.trigger_parent_calculation() # Can make UI slow if many rows

    def update_calculations(self):
        if self.boq_item_link:
            # Fetch details from BOQ Item if not already fetched by 'fetch_from'
            # This can be redundant if fetch_from is working correctly.
            # boq_item = frappe.get_doc("Bill of Quantities Item", self.boq_item_link) # Potential performance hit
            # self.contract_quantity = boq_item.quantity
            # self.unit_rate = boq_item.unit_rate
            # self.contract_amount = boq_item.amount
            pass # Assuming fetch_from handles these

        self.cumulative_quantity_executed = flt(self.previous_quantity_executed) + flt(self.quantity_executed_this_period)

        if flt(self.contract_quantity) > 0:
            self.percentage_complete = (flt(self.cumulative_quantity_executed) / flt(self.contract_quantity)) * 100
        else:
            self.percentage_complete = 0

        self.value_of_work_done_this_period = flt(self.quantity_executed_this_period) * flt(self.unit_rate)
        self.cumulative_value_of_work_done = flt(self.cumulative_quantity_executed) * flt(self.unit_rate)

        if self.cumulative_quantity_executed > self.contract_quantity :
            frappe.msgprint(f"Row {self.idx}: Cumulative quantity ({self.cumulative_quantity_executed}) for '{self.boq_item_description}' exceeds contract quantity ({self.contract_quantity}).", indicator="orange", title="Warning")


    def trigger_parent_calculation(self):
        if self.parenttype == "Payment Certificate" and self.parent:
            parent_doc = frappe.get_doc(self.parenttype, self.parent)
            if hasattr(parent_doc, 'calculate_payment_summary'):
                parent_doc.calculate_payment_summary()
                # Do not save parent here. Frappe marks parent dirty. User saves.

    # Method to fetch previous certified quantities (this is complex and depends on how previous certs are tracked)
    # This should ideally be called when boq_item_link is set/changed.
    # @frappe.whitelist() # if called from client script
    def fetch_previous_certified_quantity(self):
        if not self.boq_item_link or not self.parent or not self.get("parenttype") == "Payment Certificate":
            self.previous_quantity_executed = 0
            return

        parent_cert = frappe.get_doc("Payment Certificate", self.parent)

        # Sum 'cumulative_quantity_executed' from all 'Approved' or 'Paid' Payment Certificate Progress Items
        # for the same boq_item_link on the same project, with certificate_date before current parent's date.
        # This is a simplified version assuming we look at the immediate previous certificate or a summary field.
        # A more robust way is to sum up from all *previous* certificates.

        # For true accuracy, this needs to query all *submitted and older* certificates for this project and BOQ item.
        # Let's assume for now this is either manually entered, or fetched from a "Last Approved Certificate"
        # This logic can become very complex if not managed carefully.
        # One common approach: Store cumulative quantities on the BOQ Item master itself, updated by each approved certificate.
        # Or, on creating a new certificate, iterate over the *last approved* certificate for the project.

        # Simplified: Get from the 'less_previous_payments' field if it represents sum of previous items,
        # or find the latest approved certificate for this project.
        # This is a placeholder for more detailed logic.
        # For example, if parent document has a field `previous_certificate_docname`:
        # if parent_cert.previous_certificate_docname:
        #    prev_cert_items = frappe.get_all("Payment Certificate Progress Item",
        #        filters={"parent": parent_cert.previous_certificate_docname, "boq_item_link": self.boq_item_link},
        #        fields=["cumulative_quantity_executed"])
        #    if prev_cert_items:
        #        self.previous_quantity_executed = prev_cert_items[0].cumulative_quantity_executed
        # else:
        #    self.previous_quantity_executed = 0

        # This is often handled by a "Get Items from Previous Certificate" button on the Payment Certificate.
        # For now, previous_quantity_executed is assumed to be correctly populated (e.g. by user or button).
        pass

pass
