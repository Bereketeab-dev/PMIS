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
