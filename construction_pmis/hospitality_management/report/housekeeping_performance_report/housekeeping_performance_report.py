import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": "Room", "fieldname": "room", "fieldtype": "Link", "options": "Room", "width": 120},
		{"label": "Trigger User (Dirty)", "fieldname": "trigger_user", "fieldtype": "Link", "options": "User", "width": 150},
		{"label": "Trigger Time", "fieldname": "trigger_time", "fieldtype": "Datetime", "width": 160},
		{"label": "Cleaning User", "fieldname": "cleaning_user", "fieldtype": "Link", "options": "User", "width": 150},
		{"label": "Cleaning Start Time", "fieldname": "cleaning_start_time", "fieldtype": "Datetime", "width": 160},
		{"label": "Cleaning End Time", "fieldname": "cleaning_end_time", "fieldtype": "Datetime", "width": 160},
		{"label": "Duration (Mins)", "fieldname": "duration", "fieldtype": "Float", "width": 120}
	]

def get_data(filters):
	# Fetch all 'Finished Cleaning' logs
	finished_logs = frappe.get_all("Housekeeping Log",
		filters={"action": "Finished Cleaning"},
		fields=["room", "user", "timestamp", "duration"],
		order_by="timestamp desc"
	)

	data = []
	for log in finished_logs:
		# Find the corresponding 'Started Cleaning' log
		started_log = frappe.get_all("Housekeeping Log",
			filters={"room": log.room, "action": "Started Cleaning", "timestamp": ["<", log.timestamp]},
			fields=["user", "timestamp"],
			order_by="timestamp desc",
			limit=1
		)

		# Find the 'Marked Dirty' log that preceded the cleaning
		dirty_log = frappe.get_all("Housekeeping Log",
			filters={"room": log.room, "action": "Marked Dirty", "timestamp": ["<", log.timestamp]},
			fields=["user", "timestamp"],
			order_by="timestamp desc",
			limit=1
		)

		row = {
			"room": log.room,
			"cleaning_user": log.user,
			"cleaning_end_time": log.timestamp,
			"duration": log.duration
		}

		if started_log:
			row["cleaning_start_time"] = started_log[0].timestamp

		if dirty_log:
			row["trigger_user"] = dirty_log[0].user
			row["trigger_time"] = dirty_log[0].timestamp

		data.append(row)

	return data
