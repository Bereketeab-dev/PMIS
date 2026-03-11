# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, nowtime

class CommissioningChecklist(Document):
    def autoname(self):
        # format:COMM-{project}-{system_name}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        system_name_abbr = self.system_name[:10].upper().replace(" ", "-") if self.system_name else "SYS"
        prefix = f"COMM-{project_abbr}-{system_name_abbr}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if not self.checklist_title:
            self.checklist_title = f"Commissioning for {self.system_name} - {self.project}"

        if self.status == "Completed" and not self.actual_commissioning_end_date:
            self.actual_commissioning_end_date = nowdate()

        if self.status == "Closed" and not self.overall_result:
            # Check if all items are 'Pass' or 'N/A' to auto-set Overall Result
            all_pass_or_na = True
            if self.commissioning_checklist_items:
                for item in self.commissioning_checklist_items:
                    if item.result_status not in ["Pass", "N/A"]:
                        all_pass_or_na = False
                        break
                if all_pass_or_na:
                    self.overall_result = "Pass"
                else:
                    # Requires manual setting if not all pass/NA, or could be Pass with Remarks
                    frappe.msgprint("Some checklist items are not 'Pass' or 'N/A'. Please set Overall Result manually.", indicator="orange")
            else: # No items, can be considered Pass if no specific checks
                 self.overall_result = "Pass"


    def before_submit(self):
        # Usually, workflow handles status changes. If submitted manually:
        if self.docstatus == 0 and self.status == "Planned":
            self.status = "Pre-Commissioning Checks" # Example starting state

    # Workflow methods could be:
    # start_pre_commissioning_checks()
    # start_functional_tests()
    # start_performance_tests()
    # complete_commissioning() -> sets status to Completed
    # close_checklist() -> sets status to Closed after review and result setting

class CommissioningChecklistItem(Document):
    def validate(self):
        if self.result_status in ["Pass", "Fail", "N/A"] and not self.verification_date:
            self.verification_date = nowdate()
            if not self.verified_by:
                self.verified_by = frappe.session.user # Default verifier

        # If parent status is being updated based on child items, that logic would be in parent's validate/update method
    pass
