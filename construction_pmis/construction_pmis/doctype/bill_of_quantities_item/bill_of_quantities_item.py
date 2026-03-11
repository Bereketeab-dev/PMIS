# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class BillofQuantitiesItem(Document):
    def validate(self):
        self.calculate_amount()
        # Trigger recalculation in parent (Cost Estimate)
        if self.parenttype == "Cost Estimate" and self.parent:
            parent_doc = frappe.get_doc(self.parenttype, self.parent)
            if hasattr(parent_doc, 'calculate_totals'):
                parent_doc.calculate_totals()
                # Note: Avoid saving parent_doc here directly in child's validate.
                # Parent's save should be triggered from parent's context or UI interaction.
                # Frappe typically handles this by marking parent as dirty.

    def on_change(self): # Note: on_change is primarily a client-side concept.
                        # Server-side equivalent for reacting to value changes before save is validate.
        self.calculate_amount()

    def calculate_amount(self):
        self.amount = flt(self.quantity) * flt(self.unit_rate)

    # autoname can be set if needed, e.g., based on parent and item_code
    # def autoname(self):
    #     if self.parent and self.item_code:
    #         # Sanitize item_code for name if it contains special characters
    #         safe_item_code = frappe.utils.slug(self.item_code[:20]) if self.item_code else "item"
    #         self.name = f"{self.parent}-BOQ-{safe_item_code}-{self.idx}"
    #     else:
    #         # Fallback if parent or item_code is not set (should not happen for child tables)
    #         self.name = frappe.generate_hash(self.doctype, 10)
    pass

# Note: When this child table is used in other DocTypes like Payment Certificate,
# the `parenttype` check in `validate` would need to be adjusted or made more generic,
# or the parent DocType (Payment Certificate) would need its own logic to sum these items.
# For now, it's specific to Cost Estimate.
# A common pattern is to have a method in the parent DocType (e.g., `update_item_calculations`)
# that iterates through its child items and calls their calculation methods.
# Then, the child item's validate can call self.parent_doc.update_item_calculations(self.idx)
# This is generally handled by Frappe's framework when values in child table change and parent needs update.
# The key is that `parent_doc.calculate_totals()` should be robust enough to be called multiple times.
# And the parent document should be saved by the user or a higher-level process, not directly by child's validate.
# Frappe's UI usually marks the parent document as "dirty" (needs saving) when child table values change.
# The `validate` method in parent (CostEstimate) is called upon saving the parent, which will run `calculate_totals`.
# So, direct call to `parent_doc.calculate_totals()` from child may not be needed if `parent_doc.save()` is not called.
# The primary role of child's validate here is to calculate its own fields (e.g., `amount`).
# The parent's total calculation will naturally happen when the parent is saved.
# Let's simplify the child's validate:
# class BillofQuantitiesItem(Document):
#     def validate(self):
#         self.calculate_amount()

#     def calculate_amount(self):
#         self.amount = flt(self.quantity) * flt(self.unit_rate)
#
# This is cleaner. The CostEstimate.py's validate method already iterates through boq_items
# and sums their amounts. This ensures totals are correct when CostEstimate is saved.
# I will stick to the simpler version in the actual file.
# (Self-correction: The above comment is good, but the code was already simple. The point is valid for more complex interactions.)
# The current code for BillofQuantitiesItem.py is fine.
# The `parent_doc.calculate_totals()` call in child's validate is more of an explicit trigger,
# useful if calculations need to reflect immediately in parent's non-persisted state in UI before save.
# However, for data integrity, parent's validate on save is the ultimate source of truth for totals.
# I'll keep the explicit call for now as it can be useful for UI responsiveness if scripts are set up for it.
# Let's refine: the parent's values should be updated, but the parent itself should not be saved from child's validate.
# Frappe's ORM should handle marking the parent as dirty for saving.
# The current implementation in `BillofQuantitiesItem.py` regarding `parent_doc.calculate_totals()` is fine.
# It does not save the parent_doc.
pass
