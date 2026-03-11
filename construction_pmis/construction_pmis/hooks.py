app_name = "construction_pmis"
app_title = "Construction PMIS"
app_publisher = "Bereketeab Dev"
app_description = "Construction Project Management Information System for ERPNext"
app_email = "bereketeabdev@gmail.com"
app_license = "MIT"
app_version = "1.0.0"

# Fixtures
fixtures = [
    {"dt": "Workflow", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Report", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Dashboard", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Number Card", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Construction PMIS"]]}
]

# Required Apps
required_apps = ["erpnext"]

# DocType Events
# Note: Redundant events removed as they are already handled in DocType class files.
doc_events = {
    # Add hooks for DocTypes from other apps here if needed
}

# Desk Config
# v14 uses Workspaces, but we can keep desktop.py for backward compatibility or transition
# app_include_python = [
# 	"construction_pmis.config.desktop"
# ]
