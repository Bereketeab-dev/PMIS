# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re # For parsing bar type and grade

class RebarBBSItem(Document):
    def validate(self):
        self.calculate_total_length()
        self.calculate_weight()

    def calculate_total_length(self):
        if self.bar_length_mm and self.number_of_bars:
            self.total_length_m = (self.bar_length_mm / 1000) * self.number_of_bars
        else:
            self.total_length_m = 0

    def calculate_weight(self):
        # Simplified weight calculation.
        # A more accurate calculation would use a rebar weight per meter table/formula based on diameter.
        # Example: Weight (kg/m) = (Diameter^2 * 0.00617) for steel
        # For now, a placeholder or a very simplified logic.
        # User might need to input this or have a linked "Rebar Type" master with weight/m.

        weight_per_meter = 0
        if self.bar_type_grade:
            # Try to extract diameter from 'T12', 'H20', etc.
            match = re.search(r'\d+', self.bar_type_grade)
            if match:
                try:
                    diameter = float(match.group(0))
                    # Using the formula: Weight (kg/m) = D^2 / 162 for steel bars (approx)
                    # Or more precisely: (pi * (D/2)^2 * density_steel) / 1000^2
                    # Density of steel approx 7850 kg/m^3
                    # Weight per meter (kg/m) = (diameter_mm^2 * pi * 7850) / (4 * 1000^2)
                    # Simplified: D^2 * 0.00617 (for D in mm)
                    weight_per_meter = (diameter ** 2) * 0.006165 # More precise factor for steel kg/m per mm^2
                except ValueError:
                    pass # Could not parse diameter

        if self.total_length_m and weight_per_meter > 0:
            self.weight_kg = self.total_length_m * weight_per_meter
        else:
            # If diameter cannot be determined, or no length, weight is 0 or could be manually entered.
            # Consider adding a manual override for weight or linking to a rebar properties master.
            self.weight_kg = 0 # Or None, if you prefer field to be empty

    # autoname can be set if needed, e.g., based on parent and bar_mark
    # def autoname(self):
    #     if self.parent and self.bar_mark:
    #         self.name = f"{self.parent}-BBS-{self.bar_mark}-{self.idx}"
pass
