app_name = "construction_pmis"
app_title = "Construction PMIS"
app_publisher = "Bereketeab Dev"
app_description = "Construction Project Management Information System for ERPNext"
app_email = "bereketeabdev@gmail.com"
app_license = "MIT"

# Apps
# ------------------

required_apps = ["erpnext"]

# Fixtures
# ------------------
fixtures = [
    {"dt": "Workflow", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Report", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Dashboard", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Number Card", "filters": [["module", "=", "Construction PMIS"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Construction PMIS"]]}
]

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
}

# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "Project Stakeholder",
        "filter_by": "email",
        "redact_fields": [],
        "partial": 1,
    }
]
