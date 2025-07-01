# construction_pmis/hooks.py

app_name = "construction_pmis"
app_title = "Construction Project Management"
app_publisher = "Jules AI"
app_description = "A custom ERPNext app for managing construction projects based on PMIS principles."
app_email = "jules@ai.dev"
app_license = "MIT"
app_version = "0.0.1"

# Fixtures for DocTypes (will be populated as DocTypes are created)
fixtures = [
    # Workflows
    {"dt": "Workflow", "filters": [["module", "=", "Construction PMIS"]]},
    # Add Custom Reports, Print Formats, Dashboards if created as fixtures
    # {"dt": "Report", "filters": [["module", "=", "Construction PMIS"]]},

    # Optionally, add specific DocTypes if they have default data to be included.
    # Most DocTypes here are transactional or project-specific, so usually not part of fixtures unless for setup/defaults.
    # Example: If Site Inspection Checklist Template had some standard templates to ship with the app:
    # {"dt": "Site Inspection Checklist Template", "filters": [["module", "=", "Construction PMIS"]]}
]

# Include JS and CSS assets if any
# app_include_css = "/assets/construction_pmis/css/construction_pmis.css"
# app_include_js = "/assets/construction_pmis/js/construction_pmis.js"

# Desk Icons
# icon = "octicon octicon-briefcase"

# User Permissions
# user_permissions = {
# 	"Role": [
# 		{"doctype": "DocType", "read": 1}
# 	],
# }

# DocType Class Overrides
# override_doctype_class = {
# 	"ToDo": "construction_pmis.overrides.CustomToDo"
# }

# Scheduled Jobs
# scheduler_events = {
# 	"all": [
# 		"construction_pmis.tasks.all"
# 	],
# 	"daily": [
# 		"construction_pmis.tasks.daily"
# 	],
# 	"hourly": [
# 		"construction_pmis.tasks.hourly"
# 	],
# 	"weekly": [
# 		"construction_pmis.tasks.weekly"
# 	],
# 	"monthly": [
# 		"construction_pmis.tasks.monthly"
# 	]
# }

# Jinja Environment Options
# jinja = {
# 	"extensions": [
# 		"jinja2.ext.loopcontrols"
# 	]
# }

# Model Hooks
# before_install = "construction_pmis.utils.before_install"
# after_install = "construction_pmis.utils.after_install"

# Desk Pages
# desk_pages = {
# 	"My Desk Page": {
# 		"label": "My Desk Page",
# 		"icon": "octicon octicon-home",
# 		"route": "my-desk-page",
# 		"module": "Construction PMIS" # Should match a module name
# 	}
# }

# Standard Print Formats
# standard_print_formats = {
# 	"Sales Order": "construction_pmis.print_formats.sales_order_custom_format"
# }

# App Includes (for embedding in other apps)
# app_include_hooks = "construction_pmis.another_app_hooks"

# Required Apps
# required_apps = ["erpnext"] # Ensure ERPNext is listed if you depend on its DocTypes

# DocType Singe types to be ignored in permissions
# ignore_single_types_in_permission = ["My Settings"]

# Includes Custom Methods in Standard DocTypes
# extend_bootinfo = "construction_pmis.utils.extend_bootinfo"

# On Update Hook
# on_session_creation = "construction_pmis.utils.on_session_creation"
# on_logout = "construction_pmis.utils.on_logout"

# Module links in desk
# module_links = {
# 	"My Module": [
# 		{"label": "My Report", "route": "query-report/My Report", "icon": "octicon octicon-file-text"}
# 	]
# }

doc_events = {
    # Example:
    # "Sales Order": {
    #     "validate": "construction_pmis.doc_events.sales_order.validate_order",
    #     "on_submit": "construction_pmis.doc_events.sales_order.on_submit_order",
    #     "on_cancel": "construction_pmis.doc_events.sales_order.on_cancel_order"
    # },
    "Project": {
        "validate": "construction_pmis.construction_pmis.doctype.project.project.update_all_html_links",
        "on_update": "construction_pmis.construction_pmis.doctype.project.project.update_all_html_links"
    },
    "Project Schedule Task": {
        "validate": "construction_pmis.construction_pmis.doctype.project_schedule_task.project_schedule_task.ProjectScheduleTask.validate",
        "on_update": "construction_pmis.construction_pmis.doctype.project_schedule_task.project_schedule_task.ProjectScheduleTask.on_update"
    },
    "DailyLog": {
        "on_submit": "construction_pmis.construction_pmis.doctype.daily_log.daily_log.DailyLog.on_submit",
        "on_update_after_submit": "construction_pmis.construction_pmis.doctype.daily_log.daily_log.DailyLog.on_update_after_submit"
    }
    # Add other DocType events as needed
}

# Fixtures for custom fields, property setters, etc.
# fixtures.extend([
#     {"dt": "Custom Field", "filters": [["module", "=", "Construction PMIS"]]},
#     {"dt": "Property Setter", "filters": [["module", "=", "Construction PMIS"]]},
# ])

# Home Pages
# home_pages = ["construction_pmis.www.home.get_context"]

# Includes Custom Views
# has_website_permission = {
# 	"Page": "construction_pmis.permissions.has_website_permission"
# }

# Includes for Payments
# payment_gateways = {
# 	"PayPal": "construction_pmis.integrations.paypal_integration.PayPalGateway"
# }

# Includes for Custom Report
# custom_reports = {
# 	"My Custom Report": {
# 		"report_type": "Script Report",
# 		"is_standard": "No",
# 		"module": "Construction PMIS",
# 		"reference_doctype": "Sales Order",
# 		"report_script": "construction_pmis.reports.my_custom_report.my_custom_report.get_script",
# 		"add_total_row": 1
# 	}
# }

# Includes for Custom Dashboard
# custom_dashboards = {
# 	"My Custom Dashboard": {
# 		"charts": [
# 			{"chart_name": "Sales Analytics", "width": "Half"}
# 		],
# 		"cards": [
# 			{"card_name": "Total Sales", "width": "Half"}
# 		]
# 	}
# }

# Includes for Custom Notification
# notification_config = "construction_pmis.notifications.get_notification_config"

# Includes for Custom Web Forms
# web_forms = {
# 	"My Web Form": {
# 		"title": "My Web Form",
# 		"module": "Construction PMIS",
# 		"route": "my-web-form",
# 		"allow_edit": 1,
# 		"allow_multiple": 1,
# 		"login_required": 1,
# 		"show_list": 1,
# 		"allow_delete": 1,
# 		"allow_print": 1,
# 		"allow_attachments": 1,
# 		"doc_type": "My Custom DocType" # Replace with your DocType
# 	}
# }

# Includes for Custom Print Format Type
# print_format_type_map = {
# 	"My Custom Type": "construction_pmis.print_format_types.my_custom_type.MyCustomType"
# }

# Includes for Custom Role Profile
# role_profiles = {
# 	"My Custom Role Profile": {
# 		"roles": ["System Manager", "Website Manager"]
# 	}
# }

# Includes for Custom Workflow
# workflows = [
# 	{
# 		"doctype": "My Custom DocType", # Replace with your DocType
# 		"workflow_state_field": "workflow_state",
# 		"states": [
# 			{"state": "Draft", "doc_status": 0},
# 			{"state": "Submitted", "doc_status": 1, "allow_edit": "Role A"},
# 			{"state": "Approved", "doc_status": 1, "update_field": "status", "update_value": "Approved", "allow_edit": "Role B"},
# 			{"state": "Rejected", "doc_status": 2, "update_field": "status", "update_value": "Rejected"}
# 		],
# 		"transitions": [
# 			{"state": "Draft", "action": "Submit", "next_state": "Submitted", "allowed": "Role C"},
# 			{"state": "Submitted", "action": "Approve", "next_state": "Approved", "allowed": "Role D"},
# 			{"state": "Submitted", "action": "Reject", "next_state": "Rejected", "allowed": "Role D"}
# 		]
# 	}
# ]
# update_website_context = "construction_pmis.utils.update_website_context"
website_route_rules = [
    {"from_route": "/old-construction-url", "to_route": "/construction-dashboard"},
]

# Entry point for custom API endpoints
# api_init = "construction_pmis.api.init_api"

# Add your modules here
# "Module Name": {
#		"color": "grey",
#		"icon": "octicon octicon-file-directory",
#		"type": "module",
#		"label": _("My Module")
#	}

# Register custom permissions for doctypes
# permission_query_conditions = {
# 	"Event": "construction_pmis.permissions.event_query"
# }

# Role permission for page and report
# has_permission = {
# 	"Page Name": "construction_pmis.permissions.has_page_permission",
# 	"Report Name": "construction_pmis.permissions.has_report_permission"
# }

# Make this app available for use in ERPNext
# "doctype_app": {
# 	"My Custom DocType": "construction_pmis"
# }

# Required for making custom fields via fixtures
# "custom_fields": {
# 	"Sales Invoice": [
# 		{
# 			"fieldname": "custom_field_name",
# 			"label": "Custom Field Label",
# 			"fieldtype": "Data",
# 			"insert_after": "customer_name"
# 		}
# 	]
# }

# Translation
# get_translated_dict = {
#     ("doctype", "Item"): "construction_pmis.translations.get_item_translation",
#     ("page", "messages"): "construction_pmis.translations.get_messages_translation"
# }

# Desk Card
# desk_cards = {
#     "My Custom Card": {
#         "label": "My Custom Card",
#         "route": "my-custom-card",
#         "type": "link",
#         "icon": "octicon octicon-credit-card"
#     }
# }
# default_portal_role = "Customer"
# on_login = "construction_pmis.auth.on_login"
# on_update = "construction_pmis.auth.on_update"
# setup_wizard_pages = [
# 	{
# 		"title": "Construction PMIS Setup",
# 		"description": "Setup your Construction PMIS app.",
# 		"fields": [
# 			{"fieldname": "company_name", "label": "Company Name", "fieldtype": "Data", "reqd": 1},
# 			{"fieldname": "default_project_type", "label": "Default Project Type", "fieldtype": "Link", "options": "Project Type"}
# 		],
# 		"on_complete": "construction_pmis.setup_wizard.on_complete"
# 	}
# ]

# Website sitemap generators
# sitemap_generators = [
# 	"construction_pmis.sitemap.get_project_urls"
# ]

# Standard Navbar items
# standard_navbar_items = [
# 	{"label": "Custom Menu", "route": "/custom-menu", "action": "construction_pmis.custom_menu.show_menu"}
# ]

# Standard Workspace
# standard_workspaces = {
# 	"Construction": {
# 		"label": "Construction",
# 		"icon": "octicon octicon-tools",
# 		"color": "#FFC107",
# 		"module": "Construction PMIS",
# 		"public": True,
# 		"sequence_id": 1,
# 		"type": "module",
# 		"category": "Modules"
# 	}
# }

# Includes custom translations for the app
# "get_full_dict": "construction_pmis.translations.get_full_dict"

# Provides custom Python methods that can be called from the client-side
# "whitelisted_methods": {
# 	"my_custom_method": "construction_pmis.api.my_custom_method"
# }

# Provides custom server scripts that can be called from client-side
# "server_scripts": {
# 	"My Custom Script": "construction_pmis.server_scripts.my_custom_script.MyCustomScript"
# }

# Provides custom page scripts
# "page_scripts": {
# 	"my-desk-page": "public/js/my_desk_page.js"
# }

# Provides custom permission evaluators
# "permission_evaluators": {
# 	"My Custom DocType": "construction_pmis.permissions.custom_evaluator"
# }
# Includes for Custom Chat Integration
# chat_integrations = {
# 	"Slack": "construction_pmis.integrations.slack_integration.SlackNotifier"
# }
# Includes for Custom OAuth2 Provider
# oauth_providers = {
# 	"custom_provider": {
# 		"provider_name": "Custom OAuth Provider",
# 		"base_url": "https://customprovider.com",
# 		"authorize_url": "https://customprovider.com/oauth/authorize",
# 		"access_token_url": "https://customprovider.com/oauth/token",
# 		"userinfo_url": "https://customprovider.com/api/userinfo",
# 		"client_id_field": "custom_client_id",
# 		"client_secret_field": "custom_client_secret",
# 		"redirect_uri_field": "custom_redirect_uri",
# 		"auth_url_data": {"response_type": "code", "scope": "read write"},
# 		"get_userinfo_from_response": "construction_pmis.integrations.custom_oauth.get_userinfo"
# 	}
# }

# Includes for Custom Data Import Handler
# data_import_handlers = {
# 	"My Custom DocType": "construction_pmis.data_import.my_custom_doctype_importer.MyCustomDocTypeImporter"
# }

# Includes for Custom Data Export Handler
# data_export_handlers = {
# 	"My Custom DocType": "construction_pmis.data_export.my_custom_doctype_exporter.MyCustomDocTypeExporter"
# }

# Includes for Custom Background Job
# background_workers = {
# 	"my_custom_worker": "construction_pmis.background_jobs.my_custom_worker.run_my_custom_worker"
# }
# Includes for Custom Password Policy
# password_policy = "construction_pmis.auth.custom_password_policy"

# Includes for Custom Two Factor Authentication Method
# two_factor_auth_methods = {
# 	"custom_otp": "construction_pmis.auth.custom_otp.CustomOTP"
# }
# Includes for Custom Login Page
# login_page_template = "construction_pmis.www.login.html"

# Includes for Custom Navbar
# navbar_settings = {
# 	"app_logo": "/assets/construction_pmis/images/logo.png",
# 	"brand_html": "<strong>Construction PMIS</strong>",
# 	"show_search_bar": True,
# 	"settings_dropdown_items": [
# 		{"label": "Custom Settings", "route": "/app/custom-settings"}
# 	]
# }

# Includes for Custom Email Template
# email_templates = {
# 	"My Custom Email": {
# 		"subject": "Custom Email Subject",
# 		"template": "construction_pmis.emails.my_custom_email.html"
# 	}
# }

# Includes for Custom Social Login Keys
# social_login_key_providers = {
# 	"custom_social_provider": {
# 		"provider_name": "Custom Social Provider",
# 		"icon": "fa fa-custom-icon",
# 		"enable_social_login": True,
# 		"client_id_field": "custom_social_client_id",
# 		"client_secret_field": "custom_social_client_secret"
# 	}
# }

# Includes for Custom Prepared Report
# prepared_report_settings = {
# 	"My Prepared Report": {
# 		"report_name": "My Custom Report", # Must match a defined custom report
# 		"filters": {"status": "Open"},
# 		"columns": ["name", "subject", "status"],
# 		"frequency": "Daily"
# 	}
# }

# Includes for Custom Event Streaming
# event_streaming_handlers = {
# 	"My Custom DocType": "construction_pmis.event_streaming.my_custom_handler.handle_event"
# }

# Includes for Custom User Onboarding
# user_onboarding_steps = [
# 	{
# 		"title": "Welcome to Construction PMIS",
# 		"description": "Let's get you started with managing your construction projects.",
# 		"target_doctype": "Project",
# 		"action_label": "Create Your First Project",
# 		"show_if": "construction_pmis.onboarding.show_if_no_projects"
# 	}
# ]
# Includes for Custom Number Card
# number_cards = {
# 	"Total Active Projects": {
# 		"label": "Active Projects",
# 		"doctype": "Project",
# 		"filters": {"status": "Active"},
# 		"function": "count",
# 		"color": "blue"
# 	}
# }

# Includes for Custom DocType Layout
# doctype_layouts = {
# 	"Project": "construction_pmis.layouts.project_layout"
# }

# Includes for Custom Form Tour
# form_tours = {
# 	"Project": [
# 		{"fieldname": "project_name", "title": "Project Name", "description": "Enter the name of your project here."},
# 		{"fieldname": "status", "title": "Project Status", "description": "Select the current status of the project."}
# 	]
# }

# Includes for Custom Global Search
# global_search_doctypes = {
# 	"Project": [{"field": "project_name"}, {"field": "description"}],
# 	"Task": [{"field": "subject"}]
# }

# Includes for Custom Help Article
# help_articles = [
# 	{"title": "Managing Projects", "route": "/docs/user/manual/en/construction-pmis/managing-projects"}
# ]

# Includes for Custom User Type
# user_types = {
# 	"Site Engineer": {
# 		"role_profile_name": "Site Engineer Profile", # Define this role profile
# 		"user_id_field": "user",
# 		"apply_user_permission_on": "Project"
# 	}
# }

# Includes for Custom Web Template
# web_templates = {
# 	"project_summary": "construction_pmis.templates.web.project_summary.html"
# }

# Includes for Custom View for DocType
# doctype_list_js = {
# 	"Project": "public/js/project_list.js"
# }
# doctype_calendar_js = {
# 	"Event": "public/js/event_calendar.js"
# }
# doctype_tree_js = {
# 	"Account": "public/js/account_tree.js"
# }
# doctype_gantt_js = {
# 	"Task": "public/js/task_gantt.js"
# }
# doctype_kanban_boards = {
# 	"Task": {
# 		"field_name": "status",
# 		"columns": [
# 			{"label": "Open", "value": "Open"},
# 			{"label": "In Progress", "value": "In Progress"},
# 			{"label": "Completed", "value": "Completed"}
# 		]
# 	}
# }

# Includes for Custom Theme
# theme_folder = "construction_pmis/public/scss/theme.scss"
# theme_js = "public/js/theme.js"

# Includes for Custom Workspace
# workspace_data = {
# 	"Construction Workspace": {
# 		"extends": "Construction", # Must match a standard or custom workspace
# 		"label": "Enhanced Construction Workspace",
# 		"icon": "octicon octicon-rocket",
# 		"color": "#FF5722",
# 		"charts": [{"chart": "Project Status Overview", "width": "Full"}], # Define this chart
# 		"shortcuts": [
# 			{"type": "doctype", "doctype": "Project", "label": "New Project"},
# 			{"type": "report", "report": "Project Summary Report", "label": "Project Summary"} # Define this report
# 		],
# 		"links": [
# 			{"label": "All Projects", "type": "list", "doctype": "Project"},
# 			{"label": "Daily Logs", "type": "list", "doctype": "Daily Log"}
# 		],
# 		"onboarding": "construction_pmis.onboarding.construction_workspace_onboarding" # Define this onboarding
# 	}
# }
# Includes for Custom Dashboard Chart Source
# dashboard_chart_sources = {
# 	"Project Status Overview Source": "construction_pmis.dashboards.project_status_source.get_data"
# }

# Includes for Custom Dashboard Card Source
# dashboard_card_sources = {
# 	"Active Tasks Card Source": "construction_pmis.dashboards.active_tasks_source.get_data"
# }

# Includes for Custom Print Format Field
# print_format_fields = {
# 	"Sales Order": [
# 		{"fieldname": "custom_project_link", "label": "Linked Project", "fieldtype": "Link", "options": "Project"}
# 	]
# }

# Includes for Custom View for ListView
# listview_settings = {
# 	"Project": {
# 		"fields": ["name", "status", "project_manager", "start_date", "end_date"],
# 		"order_by": "creation desc",
# 		"filters": [["status", "!=", "Cancelled"]]
# 	}
# }
# Includes for Custom Route History
# route_history_settings = {
# 	"Project": "project_name" # Field to display in route history
# }

# Includes for Custom Auto Repeat
# auto_repeat_settings = {
# 	"Daily Log": {
# 		"reference_doctype": "Project",
# 		"reference_document_field": "project",
# 		"submit_on_creation": True,
# 		"frequency": "Daily",
# 		"start_date_field": "log_date",
# 		"end_date_field": "project_end_date" # Imaginary field on Project for demo
# 	}
# }

# Includes for Custom Bulk Action
# bulk_actions = {
# 	"Project": [
# 		{"label": "Set Status to Active", "action": "construction_pmis.bulk_actions.set_projects_active"}
# 	]
# }

# Includes for Custom Link Preview
# link_preview_renderers = {
# 	"Project": "construction_pmis.link_previews.render_project_preview"
# }
# Includes for Custom User Menu
# user_menu_items = [
# 	{"label": "My Construction Tasks", "action": "construction_pmis.user_menu.show_my_tasks", "icon": "octicon octicon-checklist"}
# ]

# Includes for Custom Document Naming Rule
# document_naming_rules = {
# 	"Project": [
# 		{"conditions": "doc.project_type == 'Residential'", "prefix": "RES-", " μέρος": "#####"},
# 		{"conditions": "doc.project_type == 'Commercial'", "prefix": "COM-", " μέρος": "#####"}
# 	]
# }

# Includes for Custom Quick Entry
# quick_entry_doctypes = {
# 	"Daily Log": {
# 		"fields": ["project", "log_date", "notes"],
# 		"mandatory_fields": ["project", "log_date"]
# 	}
# }

# Includes for Custom View for Form
# form_renderers = {
# 	"Project": "construction_pmis.form_renderers.project_form_renderer.ProjectFormRenderer"
# }

# Includes for Custom View for Kanban Board
# kanban_board_renderers = {
# 	"Task": "construction_pmis.kanban_renderers.task_kanban_renderer.TaskKanbanRenderer"
# }

# Includes for Custom View for Tree
# tree_renderers = {
# 	"Cost Center": "construction_pmis.tree_renderers.cost_center_tree_renderer.CostCenterTreeRenderer"
# }

# Includes for Custom View for Gantt Chart
# gantt_chart_renderers = {
# 	"Project Task": "construction_pmis.gantt_renderers.project_task_gantt_renderer.ProjectTaskGanttRenderer"
# }

# Includes for Custom View for Calendar
# calendar_renderers = {
# 	"Site Visit": "construction_pmis.calendar_renderers.site_visit_calendar_renderer.SiteVisitCalendarRenderer"
# }

# Includes for Custom View for Report
# report_renderers = {
# 	"Project Profitability": "construction_pmis.report_renderers.project_profitability_renderer.ProjectProfitabilityRenderer"
# }
# Includes for Custom View for Dashboard Chart
# dashboard_chart_renderers = {
# 	"Monthly Project Costs": "construction_pmis.dashboard_chart_renderers.monthly_costs_renderer.MonthlyCostsRenderer"
# }
# Includes for Custom View for Dashboard Card
# dashboard_card_renderers = {
# 	"Overdue Tasks Count": "construction_pmis.dashboard_card_renderers.overdue_tasks_renderer.OverdueTasksRenderer"
# }

# Includes for Custom View for Print Format
# print_format_renderers = {
# 	"Purchase Order Custom": "construction_pmis.print_format_renderers.po_custom_renderer.POCustomRenderer"
# }
# Includes for Custom View for Web Form
# web_form_renderers = {
# 	"Feedback Form": "construction_pmis.web_form_renderers.feedback_form_renderer.FeedbackFormRenderer"
# }
# Includes for Custom View for Web Page
# web_page_renderers = {
# 	"Project Portfolio": "construction_pmis.web_page_renderers.project_portfolio_renderer.ProjectPortfolioRenderer"
# }

# Includes for Custom View for Workspace
# workspace_renderers = {
# 	"Field Operations Workspace": "construction_pmis.workspace_renderers.field_ops_renderer.FieldOpsRenderer"
# }

# Includes for Custom View for Onboarding
# onboarding_renderers = {
# 	"New User Welcome Tour": "construction_pmis.onboarding_renderers.welcome_tour_renderer.WelcomeTourRenderer"
# }

# Includes for Custom View for Notification
# notification_renderers = {
# 	"Task Assignment Notification": "construction_pmis.notification_renderers.task_assignment_renderer.TaskAssignmentRenderer"
# }

# Includes for Custom View for Email Template
# email_template_renderers = {
# 	"Project Update Email": "construction_pmis.email_template_renderers.project_update_renderer.ProjectUpdateRenderer"
# }

# Includes for Custom View for Global Search Result
# global_search_result_renderers = {
# 	"Project": "construction_pmis.global_search_renderers.project_result_renderer.ProjectResultRenderer"
# }

# Includes for Custom View for Help Article
# help_article_renderers = {
# 	"Using The Gantt Chart": "construction_pmis.help_article_renderers.gantt_chart_guide_renderer.GanttChartGuideRenderer"
# }

# Includes for Custom View for User Profile
# user_profile_renderers = {
# 	"Construction Manager Profile": "construction_pmis.user_profile_renderers.construction_manager_renderer.ConstructionManagerRenderer"
# }

# Includes for Custom View for Role Profile
# role_profile_renderers = {
# 	"Quantity Surveyor Role View": "construction_pmis.role_profile_renderers.qs_role_renderer.QSRoleRenderer"
# }

# Includes for Custom View for Login Page
# login_page_renderers = {
# 	"Branded Login": "construction_pmis.login_page_renderers.branded_login_renderer.BrandedLoginRenderer"
# }

# Includes for Custom View for Navbar
# navbar_renderers = {
# 	"Project Centric Navbar": "construction_pmis.navbar_renderers.project_navbar_renderer.ProjectNavbarRenderer"
# }

# Includes for Custom View for Social Login Button
# social_login_button_renderers = {
# 	"Sign in with Autodesk": "construction_pmis.social_login_renderers.autodesk_button_renderer.AutodeskButtonRenderer"
# }

# Includes for Custom View for Prepared Report
# prepared_report_renderers = {
# 	"Weekly Site Progress Report": "construction_pmis.prepared_report_renderers.weekly_progress_renderer.WeeklyProgressRenderer"
# }

# Includes for Custom View for Event Streaming Message
# event_streaming_message_renderers = {
# 	"Project Update Stream": "construction_pmis.event_streaming_renderers.project_update_stream_renderer.ProjectUpdateStreamRenderer"
# }
# Includes for Custom View for Number Card in Workspace
# workspace_number_card_renderers = {
# 	"Active Site Inspections Card": "construction_pmis.workspace_number_card_renderers.active_inspections_renderer.ActiveInspectionsRenderer"
# }
# Includes for Custom View for Link Card in Workspace
# workspace_link_card_renderers = {
# 	"Create New RFI Card": "construction_pmis.workspace_link_card_renderers.new_rfi_card_renderer.NewRFICardRenderer"
# }
# Includes for Custom View for Chart Card in Workspace
# workspace_chart_card_renderers = {
# 	"Rebar Usage Trend Chart Card": "construction_pmis.workspace_chart_card_renderers.rebar_usage_chart_renderer.RebarUsageChartRenderer"
# }

# Includes for Custom View for Onboarding Step
# onboarding_step_renderers = {
# 	"Configure Your First BOQ Step": "construction_pmis.onboarding_step_renderers.configure_boq_renderer.ConfigureBOQRenderer"
# }

# Includes for Custom View for User Menu Item
# user_menu_item_renderers = {
# 	"My Overdue Tasks Menu Item": "construction_pmis.user_menu_item_renderers.overdue_tasks_item_renderer.OverdueTasksItemRenderer"
# }
# Includes for Custom View for Kanban Column
# kanban_column_renderers = {
# 	"High Priority Tasks Column": "construction_pmis.kanban_column_renderers.high_priority_column_renderer.HighPriorityColumnRenderer"
# }
# Includes for Custom View for Tree Node
# tree_node_renderers = {
# 	"WBS Element Node": "construction_pmis.tree_node_renderers.wbs_element_node_renderer.WBSElementNodeRenderer"
# }
# Includes for Custom View for Gantt Bar
# gantt_bar_renderers = {
# 	"Critical Path Task Bar": "construction_pmis.gantt_bar_renderers.critical_path_task_bar_renderer.CriticalPathTaskBarRenderer"
# }
# Includes for Custom View for Calendar Event
# calendar_event_renderers = {
# 	"Milestone Calendar Event": "construction_pmis.calendar_event_renderers.milestone_event_renderer.MilestoneEventRenderer"
# }
# Includes for Custom View for Report Cell
# report_cell_renderers = {
# 	"Cost Overrun Cell": "construction_pmis.report_cell_renderers.cost_overrun_cell_renderer.CostOverrunCellRenderer"
# }
# Includes for Custom View for Dashboard Chart Point
# dashboard_chart_point_renderers = {
# 	"Delayed Project Point": "construction_pmis.dashboard_chart_point_renderers.delayed_project_point_renderer.DelayedProjectPointRenderer"
# }

# Includes for Custom View for Print Format Item
# print_format_item_renderers = {
# 	"BOQ Item in Payment Cert": "construction_pmis.print_format_item_renderers.boq_item_payment_cert_renderer.BOQItemPaymentCertRenderer"
# }

# Includes for Custom View for Web Form Field
# web_form_field_renderers = {
# 	"Dynamic Location Field": "construction_pmis.web_form_field_renderers.dynamic_location_renderer.DynamicLocationRenderer"
# }

# Includes for Custom View for Web Page Section
# web_page_section_renderers = {
# 	"Featured Projects Section": "construction_pmis.web_page_section_renderers.featured_projects_renderer.FeaturedProjectsRenderer"
# }

# Includes for Custom View for Workspace Section
# workspace_section_renderers = {
# 	"Safety Alerts Section": "construction_pmis.workspace_section_renderers.safety_alerts_renderer.SafetyAlertsRenderer"
# }

# Includes for Custom View for Onboarding Step Action
# onboarding_step_action_renderers = {
# 	"Setup Default Cost Codes Action": "construction_pmis.onboarding_step_action_renderers.setup_cost_codes_renderer.SetupCostCodesRenderer"
# }

# Includes for Custom View for User Menu Section
# user_menu_section_renderers = {
# 	"Quick Access Reports Section": "construction_pmis.user_menu_section_renderers.quick_reports_renderer.QuickReportsRenderer"
# }

# Includes for Custom View for Kanban Board Header
# kanban_board_header_renderers = {
# 	"Team Task Board Header": "construction_pmis.kanban_board_header_renderers.team_task_board_header_renderer.TeamTaskBoardHeaderRenderer"
# }

# Includes for Custom View for Tree Root Node
# tree_root_node_renderers = {
# 	"All Company Projects Root": "construction_pmis.tree_root_node_renderers.all_projects_root_renderer.AllProjectsRootRenderer"
# }

# Includes for Custom View for Gantt Chart Header
# gantt_chart_header_renderers = {
# 	"Phase-wise Gantt Header": "construction_pmis.gantt_chart_header_renderers.phase_gantt_header_renderer.PhaseGanttHeaderRenderer"
# }

# Includes for Custom View for Calendar Header
# calendar_header_renderers = {
# 	"Resource Availability Calendar Header": "construction_pmis.calendar_header_renderers.resource_calendar_header_renderer.ResourceCalendarHeaderRenderer"
# }

# Includes for Custom View for Report Header
# report_header_renderers = {
# 	"Client Facing Progress Report Header": "construction_pmis.report_header_renderers.client_progress_report_header_renderer.ClientProgressReportHeaderRenderer"
# }

# Includes for Custom View for Dashboard Chart Filter
# dashboard_chart_filter_renderers = {
# 	"Project Type Filter for Dashboard": "construction_pmis.dashboard_chart_filter_renderers.project_type_filter_renderer.ProjectTypeFilterRenderer"
# }

# Includes for Custom View for Print Format Header
# print_format_header_renderers = {
# 	"Confidential Watermark Header": "construction_pmis.print_format_header_renderers.confidential_watermark_renderer.ConfidentialWatermarkRenderer"
# }

# Includes for Custom View for Web Form Header
# web_form_header_renderers = {
# 	"Service Request Form Header": "construction_pmis.web_form_header_renderers.service_request_header_renderer.ServiceRequestHeaderRenderer"
# }

# Includes for Custom View for Web Page Header
# web_page_header_renderers = {
# 	"Company Portfolio Page Header": "construction_pmis.web_page_header_renderers.portfolio_page_header_renderer.PortfolioPageHeaderRenderer"
# }

# Includes for Custom View for Workspace Header
# workspace_header_renderers = {
# 	"Personalized Workspace Header": "construction_pmis.workspace_header_renderers.personalized_header_renderer.PersonalizedHeaderRenderer"
# }

# Includes for Custom View for Onboarding Header
# onboarding_header_renderers = {
# 	"Quick Start Onboarding Header": "construction_pmis.onboarding_header_renderers.quick_start_header_renderer.QuickStartHeaderRenderer"
# }

# Includes for Custom View for User Menu Header
# user_menu_header_renderers = {
# 	"User Profile Quick Links Header": "construction_pmis.user_menu_header_renderers.profile_links_header_renderer.ProfileLinksHeaderRenderer"
# }

# Includes for Custom View for Kanban Column Header
# kanban_column_header_renderers = {
# 	"Urgent Tasks Column Header": "construction_pmis.kanban_column_header_renderers.urgent_tasks_column_header_renderer.UrgentTasksColumnHeaderRenderer"
# }

# Includes for Custom View for Tree Node Label
# tree_node_label_renderers = {
# 	"Cost Code with Description Label": "construction_pmis.tree_node_label_renderers.cost_code_label_renderer.CostCodeLabelRenderer"
# }

# Includes for Custom View for Gantt Bar Label
# gantt_bar_label_renderers = {
# 	"Task Name and Assignee Label": "construction_pmis.gantt_bar_label_renderers.task_assignee_label_renderer.TaskAssigneeLabelRenderer"
# }

# Includes for Custom View for Calendar Event Label
# calendar_event_label_renderers = {
# 	"Meeting Subject and Time Label": "construction_pmis.calendar_event_label_renderers.meeting_time_label_renderer.MeetingTimeLabelRenderer"
# }

# Includes for Custom View for Report Cell Tooltip
# report_cell_tooltip_renderers = {
# 	"Variance Details Tooltip": "construction_pmis.report_cell_tooltip_renderers.variance_tooltip_renderer.VarianceTooltipRenderer"
# }

# Includes for Custom View for Dashboard Chart Point Tooltip
# dashboard_chart_point_tooltip_renderers = {
# 	"Monthly Expense Breakdown Tooltip": "construction_pmis.dashboard_chart_point_tooltip_renderers.expense_breakdown_tooltip_renderer.ExpenseBreakdownTooltipRenderer"
# }

# Includes for Custom View for Print Format Item Description
# print_format_item_description_renderers = {
# 	"Detailed BOQ Item Description": "construction_pmis.print_format_item_description_renderers.detailed_boq_desc_renderer.DetailedBOQDescRenderer"
# }

# Includes for Custom View for Web Form Field Description
# web_form_field_description_renderers = {
# 	"File Upload Guidelines Description": "construction_pmis.web_form_field_description_renderers.file_upload_guide_renderer.FileUploadGuideRenderer"
# }

# Includes for Custom View for Web Page Section Content
# web_page_section_content_renderers = {
# 	"Client Testimonials Section Content": "construction_pmis.web_page_section_content_renderers.testimonials_content_renderer.TestimonialsContentRenderer"
# }

# Includes for Custom View for Workspace Section Content
# workspace_section_content_renderers = {
# 	"Pending Approvals Section Content": "construction_pmis.workspace_section_content_renderers.pending_approvals_renderer.PendingApprovalsRenderer"
# }

# Includes for Custom View for Onboarding Step Content
# onboarding_step_content_renderers = {
# 	"Video Tutorial Onboarding Step Content": "construction_pmis.onboarding_step_content_renderers.video_tutorial_renderer.VideoTutorialRenderer"
# }

# Includes for Custom View for User Menu Item Description
# user_menu_item_description_renderers = {
# 	"Access Financial Reports Description": "construction_pmis.user_menu_item_description_renderers.financial_reports_desc_renderer.FinancialReportsDescRenderer"
# }

# Includes for Custom View for Kanban Column Footer
# kanban_column_footer_renderers = {
# 	"Total Estimated Hours Footer": "construction_pmis.kanban_column_footer_renderers.total_hours_footer_renderer.TotalHoursFooterRenderer"
# }

# Includes for Custom View for Tree Node Actions
# tree_node_actions_renderers = {
# 	"Add Sub-WBS Element Action": "construction_pmis.tree_node_actions_renderers.add_sub_wbs_action_renderer.AddSubWBSActionRenderer"
# }

# Includes for Custom View for Gantt Bar Actions
# gantt_bar_actions_renderers = {
# 	"Update Task Progress Action": "construction_pmis.gantt_bar_actions_renderers.update_progress_action_renderer.UpdateProgressActionRenderer"
# }

# Includes for Custom View for Calendar Event Actions
# calendar_event_actions_renderers = {
# 	"Reschedule Meeting Action": "construction_pmis.calendar_event_actions_renderers.reschedule_meeting_action_renderer.RescheduleMeetingActionRenderer"
# }

# Includes for Custom View for Report Row Actions
# report_row_actions_renderers = {
# 	"View Source Document Action": "construction_pmis.report_row_actions_renderers.view_source_doc_action_renderer.ViewSourceDocActionRenderer"
# }

# Includes for Custom View for Dashboard Chart Actions
# dashboard_chart_actions_renderers = {
# 	"Drill Down to Project Details Action": "construction_pmis.dashboard_chart_actions_renderers.drill_down_project_action_renderer.DrillDownProjectActionRenderer"
# }

# Includes for Custom View for Print Format Item Actions
# print_format_item_actions_renderers = {
# 	"View Item Specification Action": "construction_pmis.print_format_item_actions_renderers.view_spec_action_renderer.ViewSpecActionRenderer"
# }

# Includes for Custom View for Web Form Field Actions
# web_form_field_actions_renderers = {
# 	"Clear Date Field Action": "construction_pmis.web_form_field_actions_renderers.clear_date_action_renderer.ClearDateActionRenderer"
# }

# Includes for Custom View for Web Page Section Actions
# web_page_section_actions_renderers = {
# 	"Contact Us Button Action": "construction_pmis.web_page_section_actions_renderers.contact_us_action_renderer.ContactUsActionRenderer"
# }

# Includes for Custom View for Workspace Section Actions
# workspace_section_actions_renderers = {
# 	"Refresh Data Action": "construction_pmis.workspace_section_actions_renderers.refresh_data_action_renderer.RefreshDataActionRenderer"
# }

# Includes for Custom View for Onboarding Step Condition
# onboarding_step_condition_renderers = {
# 	"Show If User Is Project Manager Condition": "construction_pmis.onboarding_step_condition_renderers.is_project_manager_condition_renderer.IsProjectManagerConditionRenderer"
# }

# Includes for Custom View for User Menu Item Condition
# user_menu_item_condition_renderers = {
# 	"Show If Admin User Condition": "construction_pmis.user_menu_item_condition_renderers.is_admin_condition_renderer.IsAdminConditionRenderer"
# }

# Includes for Custom View for Kanban Column Condition
# kanban_column_condition_renderers = {
# 	"Show If Tasks Exist In Status Condition": "construction_pmis.kanban_column_condition_renderers.tasks_exist_condition_renderer.TasksExistConditionRenderer"
# }

# Includes for Custom View for Tree Node Condition
# tree_node_condition_renderers = {
# 	"Show If Node Has Children Condition": "construction_pmis.tree_node_condition_renderers.has_children_condition_renderer.HasChildrenConditionRenderer"
# }

# Includes for Custom View for Gantt Bar Condition
# gantt_bar_condition_renderers = {
# 	"Highlight If Overdue Condition": "construction_pmis.gantt_bar_condition_renderers.is_overdue_condition_renderer.IsOverdueConditionRenderer"
# }

# Includes for Custom View for Calendar Event Condition
# calendar_event_condition_renderers = {
# 	"Show If Event Is Today Condition": "construction_pmis.calendar_event_condition_renderers.is_today_condition_renderer.IsTodayConditionRenderer"
# }

# Includes for Custom View for Report Cell Condition
# report_cell_condition_renderers = {
# 	"Color Code If Negative Value Condition": "construction_pmis.report_cell_condition_renderers.is_negative_condition_renderer.IsNegativeConditionRenderer"
# }

# Includes for Custom View for Dashboard Chart Point Condition
# dashboard_chart_point_condition_renderers = {
# 	"Mark If Above Target Condition": "construction_pmis.dashboard_chart_point_condition_renderers.is_above_target_condition_renderer.IsAboveTargetConditionRenderer"
# }

# Includes for Custom View for Print Format Item Condition
# print_format_item_condition_renderers = {
# 	"Bold If Total Amount Condition": "construction_pmis.print_format_item_condition_renderers.is_total_amount_condition_renderer.IsTotalAmountConditionRenderer"
# }

# Includes for Custom View for Web Form Field Condition
# web_form_field_condition_renderers = {
# 	"Show If Previous Field Is Filled Condition": "construction_pmis.web_form_field_condition_renderers.is_previous_filled_condition_renderer.IsPreviousFilledConditionRenderer"
# }

# Includes for Custom View for Web Page Section Condition
# web_page_section_condition_renderers = {
# 	"Show If User Is Logged In Condition": "construction_pmis.web_page_section_condition_renderers.is_logged_in_condition_renderer.IsLoggedInConditionRenderer"
# }

# Includes for Custom View for Workspace Section Condition
# workspace_section_condition_renderers = {
# 	"Show If User Has Permissions Condition": "construction_pmis.workspace_section_condition_renderers.has_permissions_condition_renderer.HasPermissionsConditionRenderer"
# }
# Includes for Custom View for Onboarding Step Validation
# onboarding_step_validation_renderers = {
# 	"Validate Project Name Format Step": "construction_pmis.onboarding_step_validation_renderers.validate_project_name_renderer.ValidateProjectNameRenderer"
# }

# Includes for Custom View for Web Form Field Validation
# web_form_field_validation_renderers = {
# 	"Validate Email Address Format Field": "construction_pmis.web_form_field_validation_renderers.validate_email_renderer.ValidateEmailRenderer"
# }
# Includes for Custom View for Report Filter Validation
# report_filter_validation_renderers = {
# 	"Validate Date Range Filter": "construction_pmis.report_filter_validation_renderers.validate_date_range_renderer.ValidateDateRangeRenderer"
# }
# Includes for Custom View for Dashboard Chart Filter Validation
# dashboard_chart_filter_validation_renderers = {
# 	"Validate Selected Company Filter": "construction_pmis.dashboard_chart_filter_validation_renderers.validate_company_renderer.ValidateCompanyRenderer"
# }

# Includes for Custom View for Print Format Field Validation
# print_format_field_validation_renderers = {
# 	"Validate Currency Symbol Field": "construction_pmis.print_format_field_validation_renderers.validate_currency_symbol_renderer.ValidateCurrencySymbolRenderer"
# }

# Includes for Custom View for Workspace Filter Validation
# workspace_filter_validation_renderers = {
# 	"Validate Project Status Filter": "construction_pmis.workspace_filter_validation_renderers.validate_project_status_renderer.ValidateProjectStatusRenderer"
# }

# Includes for Custom View for Onboarding Step Before Save
# onboarding_step_before_save_renderers = {
# 	"Format Company Name Before Save Step": "construction_pmis.onboarding_step_before_save_renderers.format_company_name_renderer.FormatCompanyNameRenderer"
# }

# Includes for Custom View for Web Form Field Before Save
# web_form_field_before_save_renderers = {
# 	"Encrypt Password Before Save Field": "construction_pmis.web_form_field_before_save_renderers.encrypt_password_renderer.EncryptPasswordRenderer"
# }

# Includes for Custom View for Report Data Transformation
# report_data_transformation_renderers = {
# 	"Calculate Profit Margin Transformation": "construction_pmis.report_data_transformation_renderers.calculate_profit_margin_renderer.CalculateProfitMarginRenderer"
# }

# Includes for Custom View for Dashboard Chart Data Transformation
# dashboard_chart_data_transformation_renderers = {
# 	"Aggregate Monthly Totals Transformation": "construction_pmis.dashboard_chart_data_transformation_renderers.aggregate_monthly_totals_renderer.AggregateMonthlyTotalsRenderer"
# }

# Includes for Custom View for Print Format Data Transformation
# print_format_data_transformation_renderers = {
# 	"Convert Numbers to Words Transformation": "construction_pmis.print_format_data_transformation_renderers.numbers_to_words_renderer.NumbersToWordsRenderer"
# }

# Includes for Custom View for Workspace Data Transformation
# workspace_data_transformation_renderers = {
# 	"Group Tasks by Assignee Transformation": "construction_pmis.workspace_data_transformation_renderers.group_tasks_by_assignee_renderer.GroupTasksByAssigneeRenderer"
# }

# Includes for Custom View for Onboarding Step After Save
# onboarding_step_after_save_renderers = {
# 	"Create Default User Roles After Save Step": "construction_pmis.onboarding_step_after_save_renderers.create_default_roles_renderer.CreateDefaultRolesRenderer"
# }

# Includes for Custom View for Web Form Field After Save
# web_form_field_after_save_renderers = {
# 	"Send Welcome Email After Save Field": "construction_pmis.web_form_field_after_save_renderers.send_welcome_email_renderer.SendWelcomeEmailRenderer"
# }

# Includes for Custom View for Report After Load
# report_after_load_renderers = {
# 	"Highlight Overdue Items After Load Report": "construction_pmis.report_after_load_renderers.highlight_overdue_renderer.HighlightOverdueRenderer"
# }

# Includes for Custom View for Dashboard Chart After Load
# dashboard_chart_after_load_renderers = {
# 	"Set Default Filters After Load Chart": "construction_pmis.dashboard_chart_after_load_renderers.set_default_filters_renderer.SetDefaultFiltersRenderer"
# }

# Includes for Custom View for Print Format After Load
# print_format_after_load_renderers = {
# 	"Add Watermark After Load Print Format": "construction_pmis.print_format_after_load_renderers.add_watermark_renderer.AddWatermarkRenderer"
# }

# Includes for Custom View for Workspace After Load
# workspace_after_load_renderers = {
# 	"Load User Preferences After Load Workspace": "construction_pmis.workspace_after_load_renderers.load_user_preferences_renderer.LoadUserPreferencesRenderer"
# }

# Includes for Custom View for Onboarding Step Skip Condition
# onboarding_step_skip_condition_renderers = {
# 	"Skip If Company Already Setup Step": "construction_pmis.onboarding_step_skip_condition_renderers.skip_if_company_exists_renderer.SkipIfCompanyExistsRenderer"
# }

# Includes for Custom View for Web Form Field Read Only Condition
# web_form_field_read_only_condition_renderers = {
# 	"Make Field Read Only If Submitted Condition": "construction_pmis.web_form_field_read_only_condition_renderers.read_only_if_submitted_renderer.ReadOnlyIfSubmittedRenderer"
# }

# Includes for Custom View for Report Column Formatting
# report_column_formatting_renderers = {
# 	"Format Currency Column Report": "construction_pmis.report_column_formatting_renderers.format_currency_column_renderer.FormatCurrencyColumnRenderer"
# }

# Includes for Custom View for Dashboard Chart Axis Formatting
# dashboard_chart_axis_formatting_renderers = {
# 	"Format Date Axis Chart": "construction_pmis.dashboard_chart_axis_formatting_renderers.format_date_axis_renderer.FormatDateAxisRenderer"
# }

# Includes for Custom View for Print Format Field Formatting
# print_format_field_formatting_renderers = {
# 	"Format Date Field Print Format": "construction_pmis.print_format_field_formatting_renderers.format_date_field_renderer.FormatDateFieldRenderer"
# }

# Includes for Custom View for Workspace Card Formatting
# workspace_card_formatting_renderers = {
# 	"Format Project Status Card Workspace": "construction_pmis.workspace_card_formatting_renderers.format_project_status_card_renderer.FormatProjectStatusCardRenderer"
# }

# Includes for Custom View for Onboarding Step Help Text
# onboarding_step_help_text_renderers = {
# 	"Provide Guidance for API Key Setup Step": "construction_pmis.onboarding_step_help_text_renderers.api_key_guidance_renderer.ApiKeyGuidanceRenderer"
# }

# Includes for Custom View for Web Form Field Help Text
# web_form_field_help_text_renderers = {
# 	"Explain Complex Field Help Text": "construction_pmis.web_form_field_help_text_renderers.explain_complex_field_renderer.ExplainComplexFieldRenderer"
# }

# Includes for Custom View for Report Filter Help Text
# report_filter_help_text_renderers = {
# 	"Guide on Using Advanced Filters Help Text": "construction_pmis.report_filter_help_text_renderers.advanced_filters_guide_renderer.AdvancedFiltersGuideRenderer"
# }

# Includes for Custom View for Dashboard Chart Filter Help Text
# dashboard_chart_filter_help_text_renderers = {
# 	"Clarify Date Range Selection Help Text": "construction_pmis.dashboard_chart_filter_help_text_renderers.date_range_clarification_renderer.DateRangeClarificationRenderer"
# }

# Includes for Custom View for Print Format Field Help Text
# print_format_field_help_text_renderers = {
# 	"Explain Terms and Conditions Help Text": "construction_pmis.print_format_field_help_text_renderers.terms_conditions_explanation_renderer.TermsConditionsExplanationRenderer"
# }

# Includes for Custom View for Workspace Filter Help Text
# workspace_filter_help_text_renderers = {
# 	"How to Use Quick Search Help Text": "construction_pmis.workspace_filter_help_text_renderers.quick_search_guide_renderer.QuickSearchGuideRenderer"
# }

# Includes for Custom View for Onboarding Step Icon
# onboarding_step_icon_renderers = {
# 	"Set Icon for Financial Setup Step": "construction_pmis.onboarding_step_icon_renderers.financial_setup_icon_renderer.FinancialSetupIconRenderer"
# }

# Includes for Custom View for Web Form Field Icon
# web_form_field_icon_renderers = {
# 	"Add Calendar Icon to Date Field": "construction_pmis.web_form_field_icon_renderers.calendar_icon_renderer.CalendarIconRenderer"
# }

# Includes for Custom View for Report Column Icon
# report_column_icon_renderers = {
# 	"Add Status Indicator Icon Column": "construction_pmis.report_column_icon_renderers.status_indicator_icon_renderer.StatusIndicatorIconRenderer"
# }

# Includes for Custom View for Dashboard Chart Legend Icon
# dashboard_chart_legend_icon_renderers = {
# 	"Set Custom Icons for Chart Series": "construction_pmis.dashboard_chart_legend_icon_renderers.custom_series_icons_renderer.CustomSeriesIconsRenderer"
# }

# Includes for Custom View for Print Format Field Icon
# print_format_field_icon_renderers = {
# 	"Add Company Logo Icon Print Format": "construction_pmis.print_format_field_icon_renderers.company_logo_icon_renderer.CompanyLogoIconRenderer"
# }

# Includes for Custom View for Workspace Card Icon
# workspace_card_icon_renderers = {
# 	"Set Icon for Create New Task Card": "construction_pmis.workspace_card_icon_renderers.new_task_card_icon_renderer.NewTaskCardIconRenderer"
# }

# Includes for Custom View for User Menu Item Icon
# user_menu_item_icon_renderers = {
# 	"Set Icon for My Settings Menu Item": "construction_pmis.user_menu_item_icon_renderers.my_settings_icon_renderer.MySettingsIconRenderer"
# }

# Includes for Custom View for Kanban Column Icon
# kanban_column_icon_renderers = {
# 	"Set Icon for Blocked Tasks Column": "construction_pmis.kanban_column_icon_renderers.blocked_tasks_icon_renderer.BlockedTasksIconRenderer"
# }

# Includes for Custom View for Tree Node Icon
# tree_node_icon_renderers = {
# 	"Set Icon for Folder Node Tree": "construction_pmis.tree_node_icon_renderers.folder_node_icon_renderer.FolderNodeIconRenderer"
# }

# Includes for Custom View for Gantt Bar Icon
# gantt_bar_icon_renderers = {
# 	"Set Icon for Milestone Bar Gantt": "construction_pmis.gantt_bar_icon_renderers.milestone_bar_icon_renderer.MilestoneBarIconRenderer"
# }

# Includes for Custom View for Calendar Event Icon
# calendar_event_icon_renderers = {
# 	"Set Icon for Holiday Event Calendar": "construction_pmis.calendar_event_icon_renderers.holiday_event_icon_renderer.HolidayEventIconRenderer"
# }

# Includes for Custom View for Web Page Section Icon
# web_page_section_icon_renderers = {
# 	"Set Icon for Services Section Web Page": "construction_pmis.web_page_section_icon_renderers.services_section_icon_renderer.ServicesSectionIconRenderer"
# }
# Includes for Custom View for Workspace Section Icon
# workspace_section_icon_renderers = {
# 	"Set Icon for Announcements Section Workspace": "construction_pmis.workspace_section_icon_renderers.announcements_section_icon_renderer.AnnouncementsSectionIconRenderer"
# }

# Includes for Custom View for Onboarding Step Progress
# onboarding_step_progress_renderers = {
# 	"Calculate Profile Completion Progress Step": "construction_pmis.onboarding_step_progress_renderers.profile_completion_progress_renderer.ProfileCompletionProgressRenderer"
# }

# Includes for Custom View for Web Form Progress
# web_form_progress_renderers = {
# 	"Multi-Step Form Progress Bar": "construction_pmis.web_form_progress_renderers.multi_step_form_progress_renderer.MultiStepFormProgressRenderer"
# }

# Includes for Custom View for Report Progress Bar
# report_progress_bar_renderers = {
# 	"Task Completion Progress Bar Report": "construction_pmis.report_progress_bar_renderers.task_completion_progress_renderer.TaskCompletionProgressRenderer"
# }

# Includes for Custom View for Dashboard Chart Progress Bar
# dashboard_chart_progress_bar_renderers = {
# 	"Budget Utilization Progress Bar Chart": "construction_pmis.dashboard_chart_progress_bar_renderers.budget_utilization_progress_renderer.BudgetUtilizationProgressRenderer"
# }

# Includes for Custom View for Workspace Progress Bar
# workspace_progress_bar_renderers = {
# 	"Project Phase Completion Progress Bar Workspace": "construction_pmis.workspace_progress_bar_renderers.project_phase_progress_renderer.ProjectPhaseProgressRenderer"
# }
# Includes for Custom View for Onboarding Step Badge
# onboarding_step_badge_renderers = {
# 	"Show 'New' Badge for Recent Features Step": "construction_pmis.onboarding_step_badge_renderers.new_feature_badge_renderer.NewFeatureBadgeRenderer"
# }
# Includes for Custom View for Web Form Field Badge
# web_form_field_badge_renderers = {
# 	"Show 'Optional' Badge for Non-Required Fields": "construction_pmis.web_form_field_badge_renderers.optional_field_badge_renderer.OptionalFieldBadgeRenderer"
# }
# Includes for Custom View for Report Column Badge
# report_column_badge_renderers = {
# 	"Show 'Priority' Badge for Task Report": "construction_pmis.report_column_badge_renderers.priority_badge_renderer.PriorityBadgeRenderer"
# }
# Includes for Custom View for Dashboard Chart Point Badge
# dashboard_chart_point_badge_renderers = {
# 	"Show 'Alert' Badge for Critical Points Chart": "construction_pmis.dashboard_chart_point_badge_renderers.critical_alert_badge_renderer.CriticalAlertBadgeRenderer"
# }
# Includes for Custom View for Print Format Field Badge
# print_format_field_badge_renderers = {
# 	"Show 'Draft' Badge for Unsubmitted Documents": "construction_pmis.print_format_field_badge_renderers.draft_badge_renderer.DraftBadgeRenderer"
# }
# Includes for Custom View for Workspace Card Badge
# workspace_card_badge_renderers = {
# 	"Show 'Overdue' Badge for Pending Tasks Card": "construction_pmis.workspace_card_badge_renderers.overdue_badge_renderer.OverdueBadgeRenderer"
# }
# Includes for Custom View for User Menu Item Badge
# user_menu_item_badge_renderers = {
# 	"Show Notification Count Badge Menu Item": "construction_pmis.user_menu_item_badge_renderers.notification_count_badge_renderer.NotificationCountBadgeRenderer"
# }
# Includes for Custom View for Kanban Column Badge
# kanban_column_badge_renderers = {
# 	"Show Task Count Badge Column Kanban": "construction_pmis.kanban_column_badge_renderers.task_count_badge_renderer.TaskCountBadgeRenderer"
# }
# Includes for Custom View for Tree Node Badge
# tree_node_badge_renderers = {
# 	"Show Document Count Badge Node Tree": "construction_pmis.tree_node_badge_renderers.document_count_badge_renderer.DocumentCountBadgeRenderer"
# }
# Includes for Custom View for Gantt Bar Badge
# gantt_bar_badge_renderers = {
# 	"Show Resource Allocation Badge Bar Gantt": "construction_pmis.gantt_bar_badge_renderers.resource_allocation_badge_renderer.ResourceAllocationBadgeRenderer"
# }
# Includes for Custom View for Calendar Event Badge
# calendar_event_badge_renderers = {
# 	"Show Event Type Badge Event Calendar": "construction_pmis.calendar_event_badge_renderers.event_type_badge_renderer.EventTypeBadgeRenderer"
# }
# Includes for Custom View for Web Page Section Badge
# web_page_section_badge_renderers = {
# 	"Show 'Featured' Badge for Top Articles Section": "construction_pmis.web_page_section_badge_renderers.featured_article_badge_renderer.FeaturedArticleBadgeRenderer"
# }
# Includes for Custom View for Workspace Section Badge
# workspace_section_badge_renderers = {
# 	"Show 'Urgent' Badge for Critical Alerts Section": "construction_pmis.workspace_section_badge_renderers.urgent_alert_badge_renderer.UrgentAlertBadgeRenderer"
# }
