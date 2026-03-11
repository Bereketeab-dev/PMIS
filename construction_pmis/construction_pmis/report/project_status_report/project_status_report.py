# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Project Name"),
            "fieldname": "project_name",
            "fieldtype": "Link",
            "options": "Project",
            "width": 200
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Project Manager"),
            "fieldname": "project_manager",
            "fieldtype": "Link",
            "options": "User",
            "width": 150
        },
        {
            "label": _("Client"),
            "fieldname": "client_name",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "label": _("Start Date"),
            "fieldname": "start_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("End Date"),
            "fieldname": "end_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Estimated Cost"),
            "fieldname": "total_estimated_cost",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Actual Cost"),
            "fieldname": "total_actual_cost",
            "fieldtype": "Currency",
            "width": 120,
            "description": "Note: Actual cost calculation requires integration with expense/invoice bookings."
        },
        {
            "label": _("% Complete"),
            "fieldname": "percent_complete",
            "fieldtype": "Percent",
            "width": 100,
            "description": "Note: Meaningful % complete requires defined logic (e.g., from tasks, manual input, or EVM)."
        }
    ]

def get_data(filters):
    conditions = "WHERE docstatus < 2 " # Basic condition to exclude cancelled/deleted
    sql_filters = {}

    if filters:
        if filters.get("project"):
            conditions += "AND name = %(project)s "
            sql_filters["project"] = filters["project"]
        if filters.get("project_manager"):
            conditions += "AND project_manager = %(project_manager)s "
            sql_filters["project_manager"] = filters["project_manager"]
        if filters.get("status"):
            conditions += "AND status = %(status)s "
            sql_filters["status"] = filters["status"]
        if filters.get("client_name"):
            conditions += "AND client_name = %(client_name)s "
            sql_filters["client_name"] = filters["client_name"]

    # In a real scenario, percent_complete and total_actual_cost would likely come from
    # complex calculations, potentially joining with other tables (tasks, timesheets, invoices)
    # or be a manually updated field on the Project doctype.
    # For this initial report, we'll select them directly if they exist on `tabProject`.
    # If `percent_complete` is not a direct field, we might return a placeholder.

    # Check if 'percent_complete' field exists in Project Doctype
    project_meta = frappe.get_meta("Project")
    has_percent_complete_field = project_meta.has_field("percent_complete")
    percent_complete_select = "percent_complete" if has_percent_complete_field else "0 as percent_complete"


    query = f"""
        SELECT
            name as project_name,
            status,
            project_manager,
            client_name,
            start_date,
            end_date,
            total_estimated_cost,
            total_actual_cost,
            {percent_complete_select}
        FROM
            `tabProject`
        {conditions}
        ORDER BY start_date DESC
    """

    data = frappe.db.sql(query, sql_filters, as_dict=True)

    # Post-processing if needed (e.g., formatting, or if % complete was calculated here)
    # for row in data:
    #    if not has_percent_complete_field:
    #        row.percent_complete = calculate_project_percent_complete(row.project_name) # Example of calling a helper

    return data

# Placeholder for a more complex calculation if needed later
# def calculate_project_percent_complete(project_name):
#   # Logic to calculate % complete based on tasks, milestones, or EVM
#   # For example, average % complete of all active tasks linked to the project
#   tasks = frappe.get_all("Project Schedule Task",
#                          filters={"project": project_name, "status": ["!=", "Cancelled"]},
#                          fields=["percent_complete", "duration"]) # Assuming duration is a weight
#   if not tasks:
#       return 0
#
#   total_weighted_percent = 0
#   total_duration = 0
#   for task in tasks:
#       weight = task.duration or 1 # Use duration as weight, or 1 if no duration
#       total_weighted_percent += (task.percent_complete or 0) * weight
#       total_duration += weight
#
#   return (total_weighted_percent / total_duration) if total_duration > 0 else 0
