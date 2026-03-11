# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate

class PaymentCertificate(Document):
    def validate(self):
        if self.period_start_date and self.period_end_date and getdate(self.period_end_date) < getdate(self.period_start_date):
            frappe.throw("Valuation Period End Date cannot be before Start Date.")
        self.calculate_payment_summary()

    def before_submit(self):
        self.status = "Pending Approval"
        if not self.progress_items:
            frappe.throw("Cannot submit Payment Certificate without any progress items.")
        if self.total_amount_due_this_certificate < 0:
            frappe.msgprint("Total amount due is negative. Please verify calculations.", indicator="orange", title="Warning")


    def on_submit(self):
        # Potentially link to accounting: Create Sales Invoice if this is for client payment
        # Or Journal Entry if it's for internal tracking / contractor payment.
        # self.create_sales_invoice() # Example
        pass

    def on_cancel(self):
        self.status = "Cancelled"
        # Reverse any accounting entries if created.
        # if self.linked_sales_invoice:
        #    si = frappe.get_doc("Sales Invoice", self.linked_sales_invoice)
        #    if si.docstatus == 1: # Submitted
        #        si.cancel()
        #        frappe.msgprint(f"Linked Sales Invoice {self.linked_sales_invoice} cancelled.")
        #    self.db_set("linked_sales_invoice", None)
        frappe.msgprint(f"Payment Certificate {self.name} has been cancelled.")


    def calculate_payment_summary(self):
        gross_value_of_work_done = 0
        if self.progress_items:
            for item in self.progress_items:
                # Ensure item calculations are up-to-date (though item.validate should handle this)
                # item.calculate_amount() # If direct method exists on child
                gross_value_of_work_done += flt(item.cumulative_value_of_work_done)

        self.gross_value_of_work_done = gross_value_of_work_done # This is cumulative sum from items

        self.total_value_to_date = flt(self.gross_value_of_work_done) + flt(self.materials_on_site_value)
        self.value_of_work_this_period = flt(self.total_value_to_date) - flt(self.less_previous_payments)

        # Retention
        self.retention_this_period = (flt(self.value_of_work_this_period) * flt(self.retention_percentage)) / 100

        # Total retention to date: this should be sum of all previous retentions + current period's retention
        # This calculation needs a robust way to get previous total retention.
        # For simplicity, assuming less_previous_payments also implies previous retention was based on it.
        # Or, a field `total_retention_previously_held` could be used.
        # Let's assume: previous_total_retention = previous_gross_value_certified * retention_percentage
        # This is tricky without knowing the exact contract terms and previous certificate details.
        # A common way: self.total_retention_to_date = (Gross Value of Work Done to Date * Retention %)
        self.total_retention_to_date = (flt(self.gross_value_of_work_done) * flt(self.retention_percentage)) / 100

        self.net_retention_held = flt(self.total_retention_to_date) - flt(self.less_retention_released)

        # Net Amount Due (example calculation, can vary by contract)
        # Value of work this period - Retention this period + Variations + Other Adjustments
        self.net_amount_due_before_vat = (
            flt(self.value_of_work_this_period)
            - flt(self.retention_this_period)
            + flt(self.approved_variations_value)
            + flt(self.other_adjustments)
        )

        # VAT Calculation
        self.vat_amount = (flt(self.net_amount_due_before_vat) * flt(self.vat_percentage)) / 100
        self.total_amount_due_this_certificate = flt(self.net_amount_due_before_vat) + flt(self.vat_amount)


    # Custom method for workflow action "Process for Payment"
    def process_for_payment(self):
        if self.status != "Approved":
            frappe.throw("Payment Certificate must be Approved before processing for payment.")

        # Logic to create Sales Invoice or trigger payment process
        # self.create_sales_invoice()
        self.db_set("status", "Processed for Payment")
        frappe.msgprint(f"Payment Certificate {self.name} processed for payment.")

    # Custom method for workflow action "Mark as Paid"
    def mark_as_paid(self):
        if self.status != "Processed for Payment":
            frappe.throw("Payment Certificate must be 'Processed for Payment' before marking as paid.")

        self.db_set("status", "Paid")
        self.db_set("payment_date", nowdate()) # Or prompt user for actual payment date
        # self.db_set("payment_reference", "...") # Prompt user or get from Payment Entry
        frappe.msgprint(f"Payment Certificate {self.name} marked as Paid.")

    # Placeholder for fetching items from BOQ or previous certificate
    @frappe.whitelist()
    def get_items_from_boq(self):
        if not self.boq_reference:
            frappe.throw("Please select a BOQ Reference (Cost Estimate) first.")

        boq = frappe.get_doc("Cost Estimate", self.boq_reference)
        self.set("progress_items", []) # Clear existing items

        for item in boq.boq_items:
            # Here, you'd also need to fetch `previous_quantity_executed` for each item
            # This requires querying previous certificates for this project & BOQ item.
            # This is a complex part. For now, previous_quantity_executed will be 0.
            # A more complete solution would have a helper function.
            prev_qty = self.get_previous_certified_quantity_for_item(item.name)

            pi = self.append("progress_items", {})
            pi.boq_item_link = item.name # Link to the specific Bill of Quantities Item
            pi.boq_item_code = item.item_code
            pi.boq_item_description = item.description
            pi.boq_item_unit = item.unit
            pi.contract_quantity = item.quantity
            pi.unit_rate = item.unit_rate
            pi.contract_amount = item.amount
            pi.previous_quantity_executed = prev_qty
            pi.quantity_executed_this_period = 0 # User to fill this

        self.calculate_payment_summary() # Recalculate totals

    def get_previous_certified_quantity_for_item(self, boq_item_name_in_cost_estimate):
        # This is a placeholder for a complex query.
        # It needs to find all 'Approved' or 'Paid' Payment Certificates for this project,
        # that are older than the current one (if dates are set),
        # then sum up 'cumulative_quantity_executed' for the given 'boq_item_link'.

        # Simplified: For this example, it will return 0.
        # In a real system, this would be a crucial and potentially slow query if not optimized.
        # Consider storing last cumulative qty on the BOQ item itself and updating it.

        # Example sketch (not fully robust):
        # if not self.project: return 0
        # prev_certs = frappe.get_all("Payment Certificate",
        #     filters={
        #         "project": self.project,
        #         "docstatus": 1, # Submitted (Approved, Paid, etc.)
        #         "status": ["in", ["Approved", "Paid", "Processed for Payment"]],
        #         "name": ["!=", self.name], # Exclude current
        #         "certificate_date": ["<", self.certificate_date or nowdate()] # Older certs
        #     },
        #     fields=["name"]
        # )
        # total_prev_qty = 0
        # for cert_header in prev_certs:
        #     items = frappe.get_all("Payment Certificate Progress Item",
        #         filters={
        #             "parent": cert_header.name,
        #             "boq_item_link": boq_item_name_in_cost_estimate # This is the name of the BOQ item in CostEstimate.boq_items
        #         },
        #         fields=["cumulative_quantity_executed"]
        #     )
        #     if items:
        #         total_prev_qty += flt(items[0].cumulative_quantity_executed) # This logic is flawed, needs careful sum of last known cumulative.
        # This should actually find the *latest* cumulative quantity from the most recent previous cert for that item.

        # For now:
        return 0


    # autoname is set in JSON as format:PC-{project}-{#####}
    pass
