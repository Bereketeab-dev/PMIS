# Construction PMIS for ERPNext

**Version:** 0.0.1 (Alpha)

## Overview

The Construction PMIS (Project Management Information System) is a custom application for ERPNext designed to manage the lifecycle of construction projects. It provides specialized DocTypes and workflows tailored to the needs of the construction industry, covering planning, execution, quality assurance, financial tracking, and project closeout.

This app aims to streamline construction project management by integrating various processes into a single ERPNext environment.

## Features (Planned & Implemented)

*   **Project Management:**
    *   Detailed Project Setup (WBS, Client, Team, Dates)
    *   Resource Planning (Manpower, Machinery)
    *   Task Scheduling with Dependencies (`Project Schedule Task`)
    *   Daily Work Planning & Logging (`Daily Work Plan`, `Daily Log`)
*   **Pre-Construction:**
    *   Contract Document Management
    *   Rebar Modeling & BBS Linking
    *   Cost Estimation & Bill of Quantities (BOQ)
*   **Construction Execution:**
    *   Daily Progress Tracking
    *   Rebar Execution Logging
    *   Subcontract Management
*   **Financial Control:**
    *   Payment Certificate Generation (Interim & Final)
    *   Variation Order Management
    *   (Future: Detailed Job Costing Reports)
*   **Quality & Safety Assurance:**
    *   Site Inspections with customizable Checklist Templates
    *   Non-Conformance Reports (NCRs)
    *   Snag List / Punch List Management
    *   Toolbox Talk Records
*   **Project Handover & Closeout:**
    *   As-Built Drawing Management
    *   Commissioning Checklists
    *   Final Account Settlement
    *   Lessons Learned Documentation
*   **Reporting & Dashboards:**
    *   Initial Project Status Report
    *   Basic Construction Projects Dashboard
    *   (Future: Comprehensive suite of time-based, cost, resource, and quality reports)

## Installation

Please refer to the `INSTALL.md` file in this repository for detailed installation instructions for an ERPNext v14 instance.

## Usage

After installation, the "Construction PMIS" module should be available in your ERPNext desk. You can start by:

1.  Setting up Projects.
2.  Defining Cost Estimates and BOQs.
3.  Planning resources and tasks.
4.  Utilizing the various DocTypes to manage daily operations, quality, financials, etc.

## Contributing

Details on contributing to this project will be added later. For now, feedback and suggestions are welcome.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

*This app was developed by Bereketeab Philemon with assistance from an AI (Jules).*
