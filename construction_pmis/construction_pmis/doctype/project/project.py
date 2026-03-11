# Copyright (c) 2024, Jules AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Project(Document):
    # autoname is set to field:project_name in JSON, so we don't need a custom autoname method here
    # unless we want complex logic. The current implementation was empty/commented anyway.

    def validate(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            frappe.throw("End Date cannot be before Start Date.")
        self.update_all_html_links()

    def update_all_html_links(self):
        self.update_contract_links_html()
        self.update_tasks_html()

    def update_contract_links_html(self):
        # Update HTML field for Contract Documents
        contract_docs = frappe.get_all("Contract Document", filters={"project": self.name}, fields=["name", "document_name", "status"])
        if contract_docs:
            html_parts = ["<table class='table table-bordered table-condensed' style='font-size: 12px;'><thead><tr><th>Document</th><th>Status</th></tr></thead><tbody>"]
            for doc in contract_docs:
                link = frappe.utils.get_link_to_form("Contract Document", doc.name)
                html_parts.append(f"<tr><td><a href='{link}'>{doc.document_name or doc.name}</a></td><td>{doc.status or ''}</td></tr>")
            html_parts.append("</tbody></table>")
            self.contract_documents_html = "".join(html_parts)
        else:
            self.contract_documents_html = "<p>No contract documents linked yet.</p>"

    def update_tasks_html(self):
        # Update HTML field for Project Schedule Tasks
        # This is a simple example; could be enhanced with more details or direct links to tasks.
        tasks = frappe.get_all("Project Schedule Task", filters={"project": self.name}, fields=["name", "task_name", "status", "start_date", "end_date"], order_by="start_date asc", limit_page_length=10)
        if tasks:
            html_parts = ["<table class='table table-bordered table-condensed' style='font-size: 12px;'><thead><tr><th>Task</th><th>Status</th><th>Start</th><th>End</th></tr></thead><tbody>"]
            for task in tasks:
                link = frappe.utils.get_link_to_form("Project Schedule Task", task.name)
                start_date_str = str(task.start_date) if task.start_date else ""
                end_date_str = str(task.end_date) if task.end_date else ""
                html_parts.append(f"<tr><td><a href='{link}'>{task.task_name or task.name}</a></td><td>{task.status or ''}</td><td>{start_date_str}</td><td>{end_date_str}</td></tr>")

            total_tasks = frappe.db.count("Project Schedule Task", {"project": self.name})
            if total_tasks > 10:
                html_parts.append(f"<tr><td colspan='4'>And {total_tasks - 10} more tasks... <a href='/app/project-schedule-task?project={self.name}'>View All Tasks</a></td></tr>")
            html_parts.append("</tbody></table>")
            self.tasks_html = "".join(html_parts)
        else:
            self.tasks_html = "<p>No project schedule tasks linked yet. <a href='/app/project-schedule-task/new?project={self.name}'>Create New Task</a></p>"


    # Methods to calculate total_estimated_cost and total_actual_cost
    # For example:
    # def update_total_estimated_cost(self):
    #     estimates = frappe.get_all("Cost Estimate", filters={"project": self.name}, fields=["total_amount"])
    #     self.total_estimated_cost = sum(d.total_amount for d in estimates)
    #     self.save(ignore_permissions=True) # Use with caution

    # def update_total_actual_cost(self):
    #     # This would depend on how actual costs are recorded (e.g., via Purchase Invoices, Journal Entries linked to Project)
    #     # For demonstration, let's assume a direct link or a specific doctype for actuals
    #     pass

# Child DocType: Project Team Member (for internal team)
# This could be a separate DocType if more fields are needed, or simplified as below if it's just a list of users.
# If it's a separate DocType, it would have its own .json and .py file.
# For now, assuming 'Project Team Member' will be a new DocType.

# Child DocType: Project Stakeholder (for consultants, contractors)
# Similar to Project Team Member, this could be a separate DocType.
# For now, assuming 'Project Stakeholder' will be a new DocType.

# Note: The actual creation of child doctypes 'Project Team Member' and 'Project Stakeholder'
# will be separate steps. The 'options' in the Project.json for these table fields
# assume these DocTypes will be created.
pass
