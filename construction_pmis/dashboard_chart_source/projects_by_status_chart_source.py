# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe

def get_data():
    data = frappe.db.sql("""
        SELECT
            status,
            COUNT(*) as count
        FROM
            `tabProject`
        WHERE
            docstatus < 2  -- Active documents
        GROUP BY
            status
        ORDER BY
            status
    """, as_dict=True)

    if not data:
        return {
            "labels": [],
            "datasets": []
        }

    labels = [d['status'] for d in data]
    dataset_data = [d['count'] for d in data]

    return {
        "labels": labels,
        "datasets": [
            {
                "name": "Projects by Status",
                "values": dataset_data
            }
        ]
    }
