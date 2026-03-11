# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate

class FinalAccount(Document):
    def autoname(self):
        # format:FINACC-{project}-{YYYY}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        year = getdate(self.final_account_date).strftime("%Y") if self.final_account_date else getdate(nowdate()).strftime("%Y")
        prefix = f"FINACC-{project_abbr}-{year}-" # Series will be appended
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if not self.title:
            self.title = f"Final Account for {self.project} as of {self.final_account_date or nowdate()}"
        self.calculate_final_account()

    def calculate_final_account(self):
        # C. Adjusted Contract Sum
        self.adjusted_contract_sum = flt(self.original_contract_sum) + flt(self.total_approved_variations)

        # E. Amount Due in this Final Account
        self.amount_due_this_final_account = flt(self.adjusted_contract_sum) - flt(self.total_amount_previously_certified)

        # H. Remaining Retention Held
        self.remaining_retention_held = flt(self.total_retention_held) - flt(self.retention_to_be_released)

        # K. Net Final Payment Due (E + G + I - J)
        # E = Amount due this final account (which is Adjusted Contract Sum - Previously Certified)
        # G = Retention to be released
        # I = Claims by Contractor
        # J = Claims by Client / LD
        self.net_final_payment_due_before_vat = (
            flt(self.amount_due_this_final_account) +
            flt(self.retention_to_be_released) +
            flt(self.claims_by_contractor) -
            flt(self.claims_by_client_ld)
        )

        # L. VAT Amount
        self.vat_amount = (flt(self.net_final_payment_due_before_vat) * flt(self.vat_percentage)) / 100

        # M. Total Final Payment Due
        self.total_final_payment_due = flt(self.net_final_payment_due_before_vat) + flt(self.vat_amount)

    def before_submit(self):
        self.status = "Pending Agreement" # Or as per workflow

    def on_submit(self):
        # Logic after submission. e.g., if agreed, status becomes "Agreed"
        # If workflow handles this, this method might not be needed for status change.
        pass

    @frappe.whitelist()
    def populate_from_project_data(self):
        if not self.project:
            frappe.throw("Please select the Project first.")
            return

        project_doc = frappe.get_doc("Project", self.project)

        # Fetch Original Contract Sum (e.g., from the primary Cost Estimate linked to the project)
        # This requires a clear way to identify the "main" or "original" cost estimate.
        # Assuming project_doc.total_estimated_cost holds this, or find based on a flag on Cost Estimate.
        # For now, let's assume it's manually entered or fetched from a specific field.
        # self.original_contract_sum = project_doc.total_estimated_cost # Example, might need refinement

        # Fetch Total Approved Variations
        variations = frappe.get_all("Variation Order",
            filters={"project": self.project, "status": "Approved"}, # Or "Implemented"
            fields=["SUM(estimated_cost_impact) as total_impact"]
        )
        if variations and variations[0].total_impact is not None:
            self.total_approved_variations = flt(variations[0].total_impact)
        else:
            self.total_approved_variations = 0

        # Fetch Total Amount Previously Certified (from Payment Certificates)
        prev_certs = frappe.get_all("Payment Certificate",
            filters={
                "project": self.project,
                "status": ["in", ["Approved", "Paid", "Processed for Payment"]],
                "certificate_type": "Interim Payment Certificate (IPC)" # Exclude any potential "Final Certificate" type if it exists
            },
            fields=["SUM(total_amount_due_this_certificate) as total_certified"] # Or sum of gross_value_of_work_done
        )
        if prev_certs and prev_certs[0].total_certified is not None:
            self.total_amount_previously_certified = flt(prev_certs[0].total_certified)
        else:
            self.total_amount_previously_certified = 0

        # Fetch Total Retention Held (this is more complex, ideally from last IPC or summed)
        # For simplicity, user might need to verify/enter this.
        # Or, find the latest approved IPC and get its `net_retention_held` or `total_retention_to_date`.
        latest_ipc = frappe.get_all("Payment Certificate",
            filters={
                "project": self.project,
                "status": ["in", ["Approved", "Paid", "Processed for Payment"]],
                "certificate_type": "Interim Payment Certificate (IPC)"
            },
            fields=["name", "total_retention_to_date", "net_retention_held"],
            order_by="certificate_date DESC",
            limit=1
        )
        if latest_ipc:
            self.total_retention_held = flt(latest_ipc[0].total_retention_to_date) # Or net_retention_held
            self.last_payment_certificate = latest_ipc[0].name
        else:
            self.total_retention_held = 0

        self.currency = project_doc.company_currency # Assuming project has company_currency field or similar.
                                                    # Or fetch from company default.
        if not self.currency:
             self.currency = frappe.defaults.get_global_default('currency')

        self.calculate_final_account()
        frappe.msgprint("Data populated from Project records. Please review and complete remaining fields.")

    # Workflow methods
    def agree_final_account(self):
        self.db_set("status", "Agreed")

    def certify_for_payment(self):
        self.db_set("status", "Certified for Payment")
        # Potentially create final Sales Invoice here

    def mark_as_paid_and_closed(self):
        self.db_set("status", "Paid & Closed")
        # Update project status to "Closed" or "Completed"
        if self.project:
            project_doc = frappe.get_doc("Project", self.project)
            if project_doc.status != "Completed": # Check current status
                project_doc.status = "Completed" # Or a more specific "Financially Closed"
                project_doc.save(ignore_permissions=True)
                frappe.msgprint(f"Project {self.project} status updated to Completed.")

pass
