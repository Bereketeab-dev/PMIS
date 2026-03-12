import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, time_diff_in_seconds

class Room(Document):
	def validate(self):
		if self.has_value_changed("status"):
			self.log_housekeeping_status()

	def log_housekeeping_status(self):
		action_map = {
			"Dirty": "Marked Dirty",
			"Cleaning": "Started Cleaning",
			"Available": "Finished Cleaning",
			"Maintenance": "Maintenance"
		}

		action = action_map.get(self.status)
		if not action:
			return

		log = frappe.get_doc({
			"doctype": "Housekeeping Log",
			"room": self.name,
			"user": frappe.session.user,
			"action": action,
			"timestamp": now_datetime()
		})

		# Calculate duration for 'Finished Cleaning'
		if action == "Finished Cleaning":
			last_log = frappe.get_all("Housekeeping Log",
				filters={"room": self.name, "action": "Started Cleaning"},
				fields=["timestamp"],
				order_by="timestamp desc",
				limit=1
			)
			if last_log:
				diff = time_diff_in_seconds(log.timestamp, last_log[0].timestamp)
				log.duration = diff / 60.0 # in minutes

		log.insert(ignore_permissions=True)
