# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class ToolboxTalk(Document):
    def autoname(self):
        # format:TBT-{project}-{YYYY}-{MM}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        year = getdate(self.date_conducted).strftime("%Y") if self.date_conducted else getdate(nowdate()).strftime("%Y")
        month = getdate(self.date_conducted).strftime("%m") if self.date_conducted else getdate(nowdate()).strftime("%m")
        prefix = f"TBT-{project_abbr}-{year}-{month}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if self.attendees:
            self.number_of_attendees = len(self.attendees)
        else:
            self.number_of_attendees = 0

    # No complex workflow usually needed, so submit/cancel are standard.
    # If approval workflow is added via JSON, then before_submit etc. can be used.
    def before_save(self):
        if not self.is_new(): # Only for existing documents
            if self.attendees:
                self.number_of_attendees = len(self.attendees)


class ToolboxTalkAttendee(Document):
    def validate(self):
        if self.employee and not self.attendee_name:
            self.attendee_name = frappe.get_cached_value("Employee", self.employee, "employee_name")
        if self.employee and not self.company_contractor:
            self.company_contractor = frappe.get_cached_value("Employee", self.employee, "company")

    pass
