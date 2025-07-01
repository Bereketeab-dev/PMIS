import frappe

@frappe.whitelist()
def get_manpower_plan_items_for_project(doctype, txt, searchfield, start, page_len, filters):
    project_name = filters.get("project")

    # Try to get project from the parent document (Project Schedule Task) if not directly in filters
    # This is crucial when the Link field is inside a child table (Task Assigned Manpower) of Project Schedule Task
    # The 'filters' dict in get_query for a child table field might not directly contain 'project'.
    # It usually contains info about the current row's parent (e.g. parent_docname for Project Schedule Task)
    if not project_name and filters.get("parenttype") == "Project Schedule Task":
        # Assuming the field in Project Schedule Task linking to Project is named 'project'
        # And this TaskAssignedManpower table's parent field is 'parent' (which is the Project Schedule Task name)
        # The 'parent' field of TaskAssignedManpower is the name of the ProjectScheduleTask document.
        # We need to get the 'project' field from that ProjectScheduleTask document.
        task_name = filters.get("parent") # This should be the name of the parent Project Schedule Task document.
        if task_name:
            project_name = frappe.db.get_value("Project Schedule Task", task_name, "project")

    if not project_name:
        # Fallback: if called from Project Schedule Task form directly (not child table context)
    if not project_name:
        doc = filters.get("doc") # 'doc' is the parent document (Project Schedule Task)
        if doc and hasattr(doc, 'project'): # doc is a DocType object
            project_name = doc.project
        elif doc and isinstance(doc, dict) and doc.get("doctype") == "Project Schedule Task": # doc is a dict
            project_name = doc.get("project")


    if not project_name:
        # Attempt to get project from the client-side document context if available
        # This is a bit of a hack, ideally filters should be set up by the caller correctly.
        # current_form_doctype = frappe.form_dict.get("doctype")
        # current_form_docname = frappe.form_dict.get("docname")
        # if current_form_doctype == "Project Schedule Task" and current_form_docname:
        #     project_name = frappe.db.get_value("Project Schedule Task", current_form_docname, "project")

        # If still no project_name, log error and return empty
        frappe.log_error(f"Project name could not be determined for manpower plan query. Filters: {filters}", "Get Query Error")
        return []

    # Query Manpower Plan Items linked to the determined Project
    # Manpower Plan Item is a child table of the Project doctype.
    # Its 'parent' field holds the name of the Project document.
    # Its 'name' field is the unique ID of the Manpower Plan Item row.
    conditions = [
        f"mpi.parent = %(project_name)s",
        f"mpi.docstatus = 0"
    ]
    condition_values = {
        "project_name": project_name,
        "txt": "%%%s%%" % txt,
        "start": start,
        "page_len": page_len
    }

    search_fields_mpi = ["mpi.name", "mpi.resource_type"]
    if txt:
        or_conditions = " OR ".join([f"{sf} LIKE %(txt)s" for sf in search_fields_mpi])
        conditions.append(f"({or_conditions})")

    query = f"""
        SELECT mpi.name, mpi.resource_type, mpi.required_quantity, emp.employee_name
        FROM `tabManpower Plan Item` mpi
        LEFT JOIN `tabEmployee` emp ON mpi.employee = emp.name
        WHERE {" AND ".join(conditions)}
        ORDER BY mpi.resource_type
        LIMIT %(start)s, %(page_len)s
    """

    results = frappe.db.sql(query, condition_values, as_dict=True)

    # Format for Link field: value, label, description
    formatted_results = []
    for r in results:
        label = f"{r.resource_type} (Qty: {r.required_quantity})"
        if r.employee_name:
            label += f" - {r.employee_name}"
        formatted_results.append({
            "value": r.name,
            "label": label,
            "description": r.name # Or any other useful description
        })
    return formatted_results


@frappe.whitelist()
def get_bbs_items_for_rebar_log(doctype, txt, searchfield, start, page_len, filters):
    # This query is for RebarExecutionLogItem to link to RebarBBSItem
    # It needs the rebar_model_reference from the parent RebarExecutionLog

    rebar_log_name = filters.get("parent")
    rebar_model_ref = None

    if rebar_log_name and filters.get("parenttype") == "Rebar Execution Log":
        rebar_model_ref = frappe.db.get_value("Rebar Execution Log", rebar_log_name, "rebar_model_reference")

    if not rebar_model_ref:
        doc = filters.get("doc") # doc here is RebarExecutionLog
        if doc:
            rebar_model_ref = doc.get("rebar_model_reference") if isinstance(doc, dict) else doc.rebar_model_reference

    if not rebar_model_ref:
        return []

    # Query Rebar BBS Items from the specific Rebar Model
    bbs_item_conditions = [
        f"parent = %(rebar_model_ref)s",
        f"parenttype = 'Rebar Model'" # Rebar BBS Item is child of Rebar Model
    ]
    bbs_item_condition_values = {
        "rebar_model_ref": rebar_model_ref,
        "txt": "%%%s%%" % txt
    }

    search_fields_bbs = ["name", "bar_mark", "bar_type_grade", "shape_code"]
    if txt:
        or_conditions_bbs = " OR ".join([f"{sf} LIKE %(txt)s" for sf in search_fields_bbs])
        bbs_item_conditions.append(f"({or_conditions_bbs})")

    bbs_item_query = f"""
        SELECT name, bar_mark, bar_type_grade, shape_code, number_of_bars, bar_length_mm, weight_kg
        FROM `tabRebar BBS Item`
        WHERE {" AND ".join(bbs_item_conditions)}
        ORDER BY bar_mark ASC
        LIMIT %(start)s, %(page_len)s
    """
    bbs_items = frappe.db.sql(bbs_item_query, bbs_item_condition_values, as_dict=True)

    formatted_bbs_items = []
    for item in bbs_items:
        label = f"{item.bar_mark} ({item.bar_type_grade})"
        description = f"Shape: {item.shape_code or 'N/A'}, Qty: {item.number_of_bars}, Length: {item.bar_length_mm}mm, Weight: {item.weight_kg}kg"
        formatted_bbs_items.append({
            "value": item.name,
            "label": label,
            "description": description
        })
    return formatted_bbs_items


@frappe.whitelist()
def get_tasks_for_daily_plan(doctype, txt, searchfield, start, page_len, filters):
    project_name = filters.get("project")
    plan_date = filters.get("date") # Date of the Daily Work Plan

    if not project_name:
        # If called from DailyWorkPlanTask, parent is DailyWorkPlan.
        # DailyWorkPlan has project and date fields.
        dwp_name = filters.get("parent")
        if dwp_name and filters.get("parenttype") == "Daily Work Plan":
            dwp_doc = frappe.get_doc("Daily Work Plan", dwp_name)
            project_name = dwp_doc.project
            plan_date = dwp_doc.date

    if not project_name or not plan_date:
        # Fallback for direct calls if DailyWorkPlan is the main doc in filter
        doc = filters.get("doc")
        if doc: # doc can be dict or DocType
            project_name = doc.get("project") if isinstance(doc, dict) else doc.project
            plan_date = doc.get("date") if isinstance(doc, dict) else doc.date

    if not project_name or not plan_date:
        frappe.log_error(f"Project or Date not found for Daily Plan Task query. Filters: {filters}", "Get Query Error")
        return []

    # Query Project Schedule Tasks relevant for the plan_date
    task_conditions = [
        f"project = %(project_name)s",
        f"status NOT IN ('Completed', 'Cancelled')",
        f"start_date <= %(plan_date)s", # Task should have started
        # f"end_date >= %(plan_date)s" # Task can be ongoing or ending on this day
    ]
    task_condition_values = {
        "project_name": project_name,
        "plan_date": plan_date,
        "txt": "%%%s%%" % txt
    }

    search_fields_task = ["name", "task_name", "wbs_reference"]
    if txt:
        or_conditions_task = " OR ".join([f"{sf} LIKE %(txt)s" for sf in search_fields_task])
        task_conditions.append(f"({or_conditions_task})")

    task_query = f"""
        SELECT name, task_name, wbs_reference, status, end_date
        FROM `tabProject Schedule Task`
        WHERE {" AND ".join(task_conditions)}
        ORDER BY end_date ASC, name ASC
        LIMIT %(start)s, %(page_len)s
    """

    tasks = frappe.db.sql(task_query, task_condition_values, as_dict=True)

    formatted_tasks = []
    for task in tasks:
        label = task.task_name
        if task.wbs_reference:
            label += f" (WBS: {task.wbs_reference})"
        label += f" [Status: {task.status}, Ends: {task.end_date}]"
        formatted_tasks.append({
            "value": task.name,
            "label": label,
            "description": f"Scheduled End: {task.end_date}, Status: {task.status}"
        })
    return formatted_tasks


@frappe.whitelist()
def get_manpower_plan_items_for_project_daily(doctype, txt, searchfield, start, page_len, filters):
    # This function is similar to get_manpower_plan_items_for_project
    # but called from Daily Work Plan Manpower table.
    # The 'project' should be sourced from the parent Daily Work Plan document.
    project_name = None
    dwp_name = filters.get("parent") # parent of DailyWorkPlanManpower is DailyWorkPlan
    if dwp_name and filters.get("parenttype") == "Daily Work Plan":
        project_name = frappe.db.get_value("Daily Work Plan", dwp_name, "project")

    if not project_name:
        doc = filters.get("doc") # 'doc' is Daily Work Plan
        if doc:
            project_name = doc.get("project") if isinstance(doc, dict) else doc.project

    if not project_name:
        frappe.log_error(f"Project name could not be determined for DWP manpower query. Filters: {filters}", "Get Query Error")
        return []

    # Reuse the main manpower query logic by passing a modified filter
    new_filters = {"project": project_name} # We only need project to filter Manpower Plan Items
    return get_manpower_plan_items_for_project(doctype, txt, searchfield, start, page_len, new_filters)


@frappe.whitelist()
def get_machinery_plan_items_for_project_daily(doctype, txt, searchfield, start, page_len, filters):
    # Similar to above, for machinery in Daily Work Plan
    project_name = None
    dwp_name = filters.get("parent")
    if dwp_name and filters.get("parenttype") == "Daily Work Plan":
        project_name = frappe.db.get_value("Daily Work Plan", dwp_name, "project")

    if not project_name:
        doc = filters.get("doc")
        if doc:
            project_name = doc.get("project") if isinstance(doc, dict) else doc.project

    if not project_name:
        frappe.log_error(f"Project name could not be determined for DWP machinery query. Filters: {filters}", "Get Query Error")
        return []

    new_filters = {"project": project_name}
    return get_machinery_plan_items_for_project(doctype, txt, searchfield, start, page_len, new_filters)


@frappe.whitelist()
def get_daily_work_plan_for_log(doctype, txt, searchfield, start, page_len, filters):
    # This query is for linking DailyLog to DailyWorkPlan
    # It should filter DWP by project and date matching the DailyLog's project and date.
    project_name = filters.get("project")
    log_date = filters.get("date")

    if not project_name or not log_date:
        # If called from form, 'doc' might be the current DailyLog document
        doc = filters.get("doc")
        if doc:
            project_name = doc.get("project") if isinstance(doc,dict) else doc.project
            log_date = doc.get("date") if isinstance(doc,dict) else doc.date

    if not project_name or not log_date:
        frappe.log_error(f"Project or Date not found for DWP link query in Daily Log. Filters: {filters}", "Get Query Error")
        return []

    dwp_conditions = [
        f"project = %(project_name)s",
        f"date = %(log_date)s",
        f"docstatus = 1" # Typically link to submitted/approved DWP
    ]
    dwp_condition_values = {
        "project_name": project_name,
        "log_date": log_date,
        "txt": "%%%s%%" % txt
    }

    search_fields_dwp = ["name", "plan_title"]
    if txt:
        or_conditions_dwp = " OR ".join([f"{sf} LIKE %(txt)s" for sf in search_fields_dwp])
        dwp_conditions.append(f"({or_conditions_dwp})")

    dwp_query = f"""
        SELECT name, plan_title, status
        FROM `tabDaily Work Plan`
        WHERE {" AND ".join(dwp_conditions)}
        ORDER BY modified DESC
        LIMIT %(start)s, %(page_len)s
    """
    dwps = frappe.db.sql(dwp_query, dwp_condition_values, as_dict=True)

    formatted_dwps = []
    for dwp in dwps:
        label = dwp.name
        if dwp.plan_title:
            label = f"{dwp.plan_title} ({dwp.name})"
        formatted_dwps.append({
            "value": dwp.name,
            "label": label,
            "description": f"Status: {dwp.status}"
        })
    return formatted_dwps


@frappe.whitelist()
def get_daily_plan_tasks_for_log(doctype, txt, searchfield, start, page_len, filters):
    # This query is for DailyLogTaskProgress to link to DailyWorkPlanTask
    # It needs the name of the parent DailyLog, to get its linked_daily_work_plan

    daily_log_name = filters.get("parent") # Parent of DailyLogTaskProgress is DailyLog
    linked_dwp_name = None

    if daily_log_name and filters.get("parenttype") == "Daily Log":
        linked_dwp_name = frappe.db.get_value("Daily Log", daily_log_name, "linked_daily_work_plan")

    if not linked_dwp_name:
        # Fallback if called from DailyLog form context before parent is saved
        doc = filters.get("doc") # doc here is DailyLog
        if doc:
            linked_dwp_name = doc.get("linked_daily_work_plan") if isinstance(doc, dict) else doc.linked_daily_work_plan

    if not linked_dwp_name:
        # frappe.log_error(f"Linked Daily Work Plan not found for Daily Log Task query. Filters: {filters}", "Get Query Error")
        return [] # No DWP linked, so no tasks to show

    # Now query tasks from that specific Daily Work Plan
    dwp_task_conditions = [
        f"parent = %(linked_dwp_name)s",
        f"parenttype = 'Daily Work Plan'"
    ]
    dwp_task_condition_values = {
        "linked_dwp_name": linked_dwp_name,
        "txt": "%%%s%%" % txt
    }

    search_fields_dwp_task = ["name", "task_name", "wbs_reference"]
    if txt:
        or_conditions_dwp_task = " OR ".join([f"{sf} LIKE %(txt)s" for sf in search_fields_dwp_task])
        dwp_task_conditions.append(f"({or_conditions_dwp_task})")

    dwp_task_query = f"""
        SELECT name, task_name, project_schedule_task
        FROM `tabDaily Work Plan Task`
        WHERE {" AND ".join(dwp_task_conditions)}
        ORDER BY idx ASC
        LIMIT %(start)s, %(page_len)s
    """
    dwp_tasks = frappe.db.sql(dwp_task_query, dwp_task_condition_values, as_dict=True)

    formatted_dwp_tasks = []
    for task in dwp_tasks:
        label = task.task_name or task.project_schedule_task
        formatted_dwp_tasks.append({
            "value": task.name, # This is the name of the row in Daily Work Plan Task table
            "label": label,
            "description": f"DWP Task: {task.name}"
        })
    return formatted_dwp_tasks


@frappe.whitelist()
def get_dwp_manpower_for_log(doctype, txt, searchfield, start, page_len, filters):
    daily_log_name = filters.get("parent")
    linked_dwp_name = None
    if daily_log_name and filters.get("parenttype") == "Daily Log":
        linked_dwp_name = frappe.db.get_value("Daily Log", daily_log_name, "linked_daily_work_plan")
    if not linked_dwp_name: return []

    return frappe.db.sql(f"""
        SELECT name, resource_type, specific_employee, planned_quantity
        FROM `tabDaily Work Plan Manpower`
        WHERE parent = %(dwp_name)s AND parenttype = 'Daily Work Plan'
        AND (resource_type LIKE %(txt)s OR specific_employee LIKE %(txt)s OR name LIKE %(txt)s)
        ORDER BY idx LIMIT %(start)s, %(page_len)s
    """, {"dwp_name": linked_dwp_name, "txt": "%%%s%%" % txt, "start":start, "page_len":page_len}, as_list=True)

@frappe.whitelist()
def get_dwp_machinery_for_log(doctype, txt, searchfield, start, page_len, filters):
    daily_log_name = filters.get("parent")
    linked_dwp_name = None
    if daily_log_name and filters.get("parenttype") == "Daily Log":
        linked_dwp_name = frappe.db.get_value("Daily Log", daily_log_name, "linked_daily_work_plan")
    if not linked_dwp_name: return []

    # Query `tabDaily Work Plan Machinery`
    results = frappe.db.sql(f"""
        SELECT dwpm.name, dwpm.machinery_type, asset.asset_name, dwpm.planned_quantity
        FROM `tabDaily Work Plan Machinery` dwpm
        LEFT JOIN `tabAsset` asset ON dwpm.machinery_asset = asset.name
        WHERE dwpm.parent = %(dwp_name)s AND dwpm.parenttype = 'Daily Work Plan'
        AND (dwpm.machinery_type LIKE %(txt)s OR asset.asset_name LIKE %(txt)s OR dwpm.name LIKE %(txt)s)
        ORDER BY dwpm.idx LIMIT %(start)s, %(page_len)s
    """, {"dwp_name": linked_dwp_name, "txt": "%%%s%%" % txt, "start":start, "page_len":page_len}, as_dict=True)

    formatted_results = []
    for r in results:
        label = r.machinery_type or ""
        if r.asset_name:
            label += f" ({r.asset_name})" if label else r.asset_name
        label += f" (Plan Qty: {r.planned_quantity})"
        formatted_results.append({"value": r.name, "label": label.strip(), "description": r.name})
    return formatted_results


@frappe.whitelist()
def get_dwp_material_for_log(doctype, txt, searchfield, start, page_len, filters):
    daily_log_name = filters.get("parent")
    linked_dwp_name = None
    if daily_log_name and filters.get("parenttype") == "Daily Log":
        linked_dwp_name = frappe.db.get_value("Daily Log", daily_log_name, "linked_daily_work_plan")
    if not linked_dwp_name: return []

    # Query `tabDaily Work Plan Material`
    results = frappe.db.sql(f"""
        SELECT dwpmat.name, item.item_name, dwpmat.required_quantity, dwpmat.uom
        FROM `tabDaily Work Plan Material` dwpmat
        LEFT JOIN `tabItem` item ON dwpmat.item_code = item.name
        WHERE dwpmat.parent = %(dwp_name)s AND dwpmat.parenttype = 'Daily Work Plan'
        AND (item.item_name LIKE %(txt)s OR dwpmat.item_code LIKE %(txt)s OR dwpmat.name LIKE %(txt)s)
        ORDER BY dwpmat.idx LIMIT %(start)s, %(page_len)s
    """, {"dwp_name": linked_dwp_name, "txt": "%%%s%%" % txt, "start":start, "page_len":page_len}, as_dict=True)

    formatted_results = []
    for r in results:
        label = r.item_name or r.item_code
        label += f" (Plan Qty: {r.required_quantity} {r.uom or ''})"
        formatted_results.append({"value": r.name, "label": label.strip(), "description": r.name})
    return formatted_results


@frappe.whitelist()
def get_machinery_plan_items_for_project(doctype, txt, searchfield, start, page_len, filters):
    project_name = filters.get("project")

    if not project_name and filters.get("parenttype") == "Project Schedule Task":
        task_name = filters.get("parent")
        if task_name:
            project_name = frappe.db.get_value("Project Schedule Task", task_name, "project")

    if not project_name:
        doc = filters.get("doc") # 'doc' is the parent document (Project Schedule Task)
        if doc and hasattr(doc, 'project'): # doc is a DocType object
            project_name = doc.project
        elif doc and isinstance(doc, dict) and doc.get("doctype") == "Project Schedule Task": # doc is a dict
            project_name = doc.get("project")


    if not project_name:
        frappe.log_error(f"Project name could not be determined for machinery plan query. Filters: {filters}", "Get Query Error")
        return []

    conditions = [
        f"mpi.parent = %(project_name)s",
        f"mpi.docstatus = 0"
    ]
    condition_values = {
        "project_name": project_name,
        "txt": "%%%s%%" % txt,
        "start": start,
        "page_len": page_len
    }

    search_fields_machinery = ["mpi.name", "mpi.machinery_type", "asset.asset_name"]
    if txt:
        or_conditions = " OR ".join([f"{sf} LIKE %(txt)s" for sf in search_fields_machinery])
        conditions.append(f"({or_conditions})")

    query = f"""
        SELECT mpi.name, mpi.machinery_type, asset.asset_name, mpi.required_quantity
        FROM `tabMachinery Plan Item` mpi
        LEFT JOIN `tabAsset` asset ON mpi.machinery_asset = asset.name
        WHERE {" AND ".join(conditions)}
        ORDER BY mpi.machinery_type, asset.asset_name
        LIMIT %(start)s, %(page_len)s
    """
    results = frappe.db.sql(query, condition_values, as_dict=True)

    formatted_results = []
    for r in results:
        label = r.machinery_type or ""
        if r.asset_name:
            label += f" ({r.asset_name})" if label else r.asset_name
        label += f" (Qty: {r.required_quantity})"

        formatted_results.append({
            "value": r.name,
            "label": label.strip(),
            "description": r.name
        })
    return formatted_results
