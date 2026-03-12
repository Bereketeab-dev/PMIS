import frappe
import unittest
from frappe.utils import now_datetime, add_to_date

class TestRoom(unittest.TestCase):
	def test_housekeeping_log_creation(self):
		hotel = frappe.get_doc({
			"doctype": "Hotel",
			"hotel_name": "Test Hotel",
			"company": "Test Company"
		}).insert(ignore_if_duplicate=True)

		room_type = frappe.get_doc({
			"doctype": "Room Type",
			"type_name": "Standard",
			"capacity": 2
		}).insert(ignore_if_duplicate=True)

		room = frappe.get_doc({
			"doctype": "Room",
			"room_number": "101",
			"room_type": "Standard",
			"hotel": "Test Hotel",
			"status": "Available"
		}).insert(ignore_if_duplicate=True)

		# Change status to Dirty
		room.status = "Dirty"
		room.save()

		log = frappe.get_all("Housekeeping Log",
			filters={"room": "101", "action": "Marked Dirty"},
			fields=["name"]
		)
		self.assertTrue(len(log) > 0)

		# Change status to Cleaning
		room.status = "Cleaning"
		room.save()

		# Change status to Available and check duration
		room.status = "Available"
		room.save()

		last_log = frappe.get_all("Housekeeping Log",
			filters={"room": "101", "action": "Finished Cleaning"},
			fields=["duration"],
			order_by="timestamp desc",
			limit=1
		)
		self.assertTrue(len(last_log) > 0)
