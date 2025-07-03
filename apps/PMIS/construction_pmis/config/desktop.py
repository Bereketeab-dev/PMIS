from frappe import _

def get_data():
    return [
        {
            "module_name": "Construction PMIS",
            "color": "#0069D9", # A shade of blue, can be changed
            "icon": "octicon octicon-tools", # Standard construction/tools icon
            "type": "module",
            "label": _("Construction PMIS"),
            "description": "Project Management Information System for Construction Projects.",
            "onboard_present": 0, # Set to 1 if you create an onboarding process
            "idx": 7, # Adjust index as per desired position on desk
            "links": [
                # Workspace (Primary Entry Point)
                {
                    "type": "Dashboard",
                    "name": "Construction Projects Dashboard", # Name of the Dashboard created
                    "label": _("Projects Dashboard"),
                    "icon": "octicon octicon-dashboard",
                    "dependencies": ["Project"]
                },
                # Key DocTypes - Section 1: Project Core
                {
                    "type": "section",
                    "label": _("Project Core")
                },
                {
                    "type": "doctype",
                    "name": "Project",
                    "label": _("Projects"),
                    "icon": "octicon octicon-briefcase",
                    "description": _("Manage construction projects.")
                },
                {
                    "type": "doctype",
                    "name": "Project Schedule Task",
                    "label": _("Project Schedule Tasks"),
                    "icon": "octicon octicon-checklist",
                    "description": _("Detailed project task scheduling.")
                },
                {
                    "type": "doctype",
                    "name": "Daily Work Plan",
                    "label": _("Daily Work Plans"),
                    "icon": "octicon octicon-calendar",
                    "description": _("Plan daily site activities.")
                },
                {
                    "type": "doctype",
                    "name": "Daily Log",
                    "label": _("Daily Logs"),
                    "icon": "octicon octicon-note",
                    "description": _("Record daily site progress and events.")
                },
                # Key DocTypes - Section 2: Financial & Contracts
                {
                    "type": "section",
                    "label": _("Financial & Contracts")
                },
                {
                    "type": "doctype",
                    "name": "Cost Estimate",
                    "label": _("Cost Estimates (BOQ)"),
                    "icon": "octicon octicon-file-spreadsheet",
                    "description": _("Manage project cost estimates and BOQs.")
                },
                {
                    "type": "doctype",
                    "name": "Payment Certificate",
                    "label": _("Payment Certificates"),
                    "icon": "octicon octicon-credit-card",
                    "description": _("Manage interim and final payment certificates.")
                },
                {
                    "type": "doctype",
                    "name": "Variation Order",
                    "label": _("Variation Orders"),
                    "icon": "octicon octicon-milestone",
                    "description": _("Manage project variations and change orders.")
                },
                {
                    "type": "doctype",
                    "name": "Subcontract",
                    "label": _("Subcontracts"),
                    "icon": "octicon octicon-organization",
                    "description": _("Manage subcontractor agreements.")
                },
                {
                    "type": "doctype",
                    "name": "Final Account",
                    "label": _("Final Accounts"),
                    "icon": "octicon octicon-repo-push", # Icon suggesting finality
                    "description": _("Manage project financial closeout.")
                },
                # Key DocTypes - Section 3: Quality & Safety
                {
                    "type": "section",
                    "label": _("Quality & Safety")
                },
                {
                    "type": "doctype",
                    "name": "Site Inspection",
                    "label": _("Site Inspections"),
                    "icon": "octicon octicon-eye",
                    "description": _("Record site quality and safety inspections.")
                },
                {
                    "type": "doctype",
                    "name": "NCR",
                    "label": _("Non-Conformance Reports (NCR)"),
                    "icon": "octicon octicon-alert",
                    "description": _("Manage non-conformances.")
                },
                {
                    "type": "doctype",
                    "name": "Snag List Item",
                    "label": _("Snag List / Punch List"),
                    "icon": "octicon octicon-issue-opened",
                    "description": _("Track project snags and defects.")
                },
                {
                    "type": "doctype",
                    "name": "Toolbox Talk",
                    "label": _("Toolbox Talks"),
                    "icon": "octicon octicon-megaphone",
                    "description": _("Record safety toolbox talks.")
                },
                # Reports Section
                {
                    "type": "section",
                    "label": _("Reports")
                },
                {
                    "type": "report",
                    "name": "Project Status Report", # Matches the report_name in project_status_report.json
                    "label": _("Project Status Report"),
                    "doctype": "Project", # The reference doctype for the report
                    "is_query_report": False # It's a Script Report
                },
                # Add links to other key reports as they are created
                # Example:
                # {
                #     "type": "report",
                #     "name": "Job Costing Detail Report",
                #     "label": _("Job Costing Detail"),
                #     "doctype": "Project",
                #     "is_query_report": False
                # },
                # Setup & Masters Section
                {
                    "type": "section",
                    "label": _("Setup & Masters")
                },
                {
                    "type": "doctype",
                    "name": "Site Inspection Checklist Template",
                    "label": _("Inspection Checklist Templates"),
                    "icon": "octicon octicon-file-submodule",
                    "description": _("Define templates for site inspections.")
                },
                {
                    "type": "doctype",
                    "name": "Rebar Model",
                    "label": _("Rebar Models (BBS)"),
                    "icon": "octicon octicon-circuit-board",
                    "description": _("Manage rebar models and BBS data.")
                },
                {
                    "type": "doctype",
                    "name": "Contract Document",
                    "label": _("Contract Documents"),
                    "icon": "octicon octicon-file-zip",
                    "description": _("Manage project contract documents.")
                },
                 {
                    "type": "doctype",
                    "name": "As-Built Drawing",
                    "label": _("As-Built Drawings"),
                    "icon": "octicon octicon-file-media",
                    "description": _("Manage As-Built Drawings.")
                },
                {
                    "type": "doctype",
                    "name": "Commissioning Checklist",
                    "label": _("Commissioning Checklists"),
                    "icon": "octicon octicon-tasklist",
                    "description": _("Manage system commissioning.")
                },
                {
                    "type": "doctype",
                    "name": "Lessons Learned",
                    "label": _("Lessons Learned"),
                    "icon": "octicon octicon-book",
                    "description": _("Document project lessons learned.")
                }
            ]
        }
    ]
