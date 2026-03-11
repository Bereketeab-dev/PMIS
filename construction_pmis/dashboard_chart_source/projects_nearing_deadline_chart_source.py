# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, add_days

def get_data():
    today = nowdate()
    next_30_days = add_days(today, 30)

    data = frappe.db.sql("""
        SELECT
            name,
            end_date
        FROM
            `tabProject`
        WHERE
            docstatus < 2  -- Active documents
            AND status NOT IN ('Completed', 'Cancelled', 'On Hold')
            AND end_date BETWEEN %(today)s AND %(next_30_days)s
        ORDER BY
            end_date ASC
    """, {"today": today, "next_30_days": next_30_days}, as_dict=True)

    if not data:
        return {
            "labels": ["No projects nearing deadline in next 30 days"],
            "datasets": [{"name": "Projects", "values": [0]}] # Placeholder for empty state
        }

    labels = [f"{d['name']} ({d['end_date']})" for d in data]
    # For a bar chart showing count, or just listing them.
    # If it's a count of projects per day, more aggregation is needed.
    # For now, let's assume we want to show a count of how many projects are due soon.
    # Or, a bar chart where each bar is a project, and height is e.g., days remaining (more complex).
    # Let's simplify: a list of projects. The chart type in JSON will determine how this is best displayed.
    # A "Bar" chart might show each project name on X-axis and a constant value (e.g., 1) on Y-axis, effectively listing them.

    # For a simple count on Y axis:
    # dataset_data = [1 for _ in data] # Each project is one bar

    # For the dashboard chart to be meaningful as a "Bar" chart from this source,
    # it typically expects labels and corresponding numerical values.
    # Let's return the count of projects for simplicity for a bar chart.
    # The labels could be the project names, and values could be a constant or days remaining.
    # Or, more simply, a count of projects. Let's use names as labels and a constant value for now for display.

    dataset_data = [1] * len(data) # Dummy value for each project to show on chart

    return {
        "labels": labels,
        "datasets": [
            {
                "name": "Projects Nearing Deadline (Next 30 Days)",
                "values": dataset_data
            }
        ]
    }
