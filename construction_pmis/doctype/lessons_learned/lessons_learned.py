# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class LessonsLearned(Document):
    def autoname(self):
        # format:LL-{project}-{YYYY}-{MM}-{#####}
        project_abbr = frappe.get_cached_value('Project', self.project, 'project_name')[:5].upper() if self.project else "PROJ"
        year = getdate(self.date_recorded).strftime("%Y") if self.date_recorded else getdate(nowdate()).strftime("%Y")
        month = getdate(self.date_recorded).strftime("%m") if self.date_recorded else getdate(nowdate()).strftime("%m")
        prefix = f"LL-{project_abbr}-{year}-{month}-"
        from frappe.model.naming import make_autoname
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        if not self.lesson_summary:
            # Create a default summary if empty, though it's a required field.
            self.lesson_summary = f"Lesson for {self.project} recorded on {self.date_recorded}"

    # No complex server-side logic usually needed for Lessons Learned beyond standard save.
    # It's primarily a knowledge repository.
pass
