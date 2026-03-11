# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ProjectTaskPredecessor(Document):
	def validate(self):
		if self.parent == self.predecessor_task:
			frappe.throw(f"Task cannot be a predecessor to itself (Row {self.idx}).")
		# Add more complex circular dependency checks if necessary, though this can be computationally expensive.
		# Basic check is often sufficient for UI-driven entries.
		pass
