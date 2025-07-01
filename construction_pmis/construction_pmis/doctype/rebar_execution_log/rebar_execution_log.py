# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate
import re # For parsing diameter

class RebarExecutionLog(Document):
    def autoname(self):
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        current_date_str = getdate(self.date).strftime("%Y%m%d") if self.date else nowdate().replace("-","")
        self.name = f"REL-{project_abbr}-{current_date_str}-"

    def validate(self):
        if not self.title:
            self.title = f"Rebar Log for {self.project} on {self.date}"
        self.calculate_totals()

    def calculate_totals(self):
        total_placed_kg = 0
        total_cut_bent_kg = 0
        total_wastage_kg = 0

        for item in self.rebar_items_log:
            # Ensure item calculations are done first
            item.calculate_weights() # Call child's method
            total_placed_kg += flt(item.weight_placed_kg)
            total_cut_bent_kg += flt(item.weight_cut_bent_kg)
            total_wastage_kg += flt(item.wastage_offcuts_kg)

        self.total_rebar_placed_kg = total_placed_kg
        self.total_rebar_cut_bent_kg = total_cut_bent_kg
        self.total_wastage_kg = total_wastage_kg

        if flt(self.total_rebar_cut_bent_kg) > 0: # Avoid division by zero
            # Wastage percentage based on what was cut/bent vs what was wasted from that
            # Or it could be (total_wastage_kg / (total_rebar_placed_kg + total_wastage_kg)) * 100
            # The definition of wastage % can vary.
            # Let's use: Wastage / (Placed + Wastage)
            denominator = flt(self.total_rebar_placed_kg) + flt(self.total_wastage_kg)
            if denominator > 0:
                 self.wastage_percentage = (flt(self.total_wastage_kg) / denominator) * 100
            else:
                 self.wastage_percentage = 0
        else:
            self.wastage_percentage = 0

    def before_submit(self):
        self.status = "Submitted"

    # on_submit can be used to update inventory if rebar is tracked as stock item.
    # For now, this log is for tracking and reporting.

class RebarExecutionLogItem(Document):
    def validate(self):
        if self.rebar_bbs_item_ref:
            # Fetch details from BBS item if not already done by client-side fetch_from
            bbs_item = frappe.get_doc("Rebar BBS Item", self.rebar_bbs_item_ref)
            self.bar_mark = bbs_item.bar_mark
            self.bar_type_grade = bbs_item.bar_type_grade
            # Try to parse diameter from bar_type_grade if not explicitly set
            if not self.diameter_mm and self.bar_type_grade:
                match = re.search(r'\d+', self.bar_type_grade)
                if match:
                    try:
                        self.diameter_mm = float(match.group(0))
                    except ValueError:
                        pass
            # If weight_cut_bent_kg is empty but quantity_cut_bent_nos is present, try to use BBS item's unit weight
            if not self.weight_cut_bent_kg and self.quantity_cut_bent_nos and bbs_item.weight_kg and bbs_item.number_of_bars:
                unit_weight_kg = flt(bbs_item.weight_kg) / flt(bbs_item.number_of_bars) if bbs_item.number_of_bars else 0
                self.weight_cut_bent_kg = flt(self.quantity_cut_bent_nos) * unit_weight_kg

        self.calculate_weights() # Call self calculation

    def calculate_weights(self):
        # Calculate weight_placed_kg if quantity_placed_nos and diameter_mm are available
        # This uses a generic weight calculation if BBS data isn't fully used or available.
        if self.quantity_placed_nos and self.diameter_mm:
            # Weight (kg/m) = (Diameter_mm^2 * 0.006165)
            # Assuming an average length if not specified, or this calculation might be too rough.
            # For better accuracy, length_per_bar is needed.
            # If rebar_bbs_item_ref is present, use its unit weight.
            unit_weight_kg = 0
            if self.rebar_bbs_item_ref:
                bbs_item_doc = frappe.get_doc("Rebar BBS Item", self.rebar_bbs_item_ref)
                if bbs_item_doc.number_of_bars and bbs_item_doc.weight_kg : # Ensure BBS item has valid data
                     unit_weight_kg = flt(bbs_item_doc.weight_kg) / flt(bbs_item_doc.number_of_bars)

            if unit_weight_kg > 0 :
                 self.weight_placed_kg = flt(self.quantity_placed_nos) * unit_weight_kg
            else:
                # Fallback if no BBS unit weight: use diameter (less accurate without length)
                # This part is problematic without bar length.
                # For now, let's assume weight_placed_kg is derived from weight_cut_bent_kg minus wastage related to placement,
                # or it's based on a more direct measurement or detailed BBS.
                # If weight_cut_bent_kg is available, placed weight should be related to it.
                # For simplicity: if Qty Placed is entered, and Qty Cut/Bent is known,
                # assume placed items are a subset of cut/bent items.
                if self.weight_cut_bent_kg and self.quantity_cut_bent_nos and flt(self.quantity_cut_bent_nos) > 0 :
                    unit_weight_from_cut = flt(self.weight_cut_bent_kg) / flt(self.quantity_cut_bent_nos)
                    self.weight_placed_kg = flt(self.quantity_placed_nos) * unit_weight_from_cut
                else: # Cannot calculate accurately
                    pass # Keep manual or set to 0 if preferred

        # If weight_cut_bent_kg is entered but quantity_cut_bent_nos is not, try to infer if diameter is present
        # (This might be too complex for basic validation, better to ensure user enters consistent data)

        # Trigger parent calculation
        if self.parenttype == "Rebar Execution Log" and self.parent:
            parent_doc = frappe.get_doc(self.parenttype, self.parent)
            if hasattr(parent_doc, 'calculate_totals'):
                parent_doc.calculate_totals()
    pass
