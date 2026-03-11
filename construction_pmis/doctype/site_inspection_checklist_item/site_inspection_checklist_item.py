from frappe.model.document import Document

class SiteInspectionChecklistItem(Document):
    def validate(self):
        if self.observation_status == "Fail" and not self.corrective_action_needed:
            self.corrective_action_needed = 1 # Auto-check if status is Fail
        elif self.observation_status == "Pass" and self.corrective_action_needed:
             self.corrective_action_needed = 0 # Uncheck if status is Pass
