# Construction PMIS App - Installation Guide for ERPNext v14

This guide provides instructions on how to install the `construction_pmis` custom app into an existing ERPNext v14 instance.

## Prerequisites

1.  **ERPNext v14 Instance:** You must have a running ERPNext v14 site.
2.  **Bench CLI:** The Frappe Bench command-line interface must be installed and configured for your ERPNext instance.
3.  **Git:** Git must be installed on the server where your ERPNext instance is hosted.
4.  **App Repository:** Access to the Git repository containing the `construction_pmis` app. Let's assume the repository URL is `[YOUR_APP_GIT_REPOSITORY_URL]`.

## Installation Steps

1.  **Navigate to your Bench Directory:**
    Open a terminal or SSH into your server and navigate to your bench directory (e.g., `frappe-bench`).
    ```bash
    cd ~/frappe-bench
    ```

2.  **Download the App:**
    Use the `bench get-app` command to download the app from its Git repository.
    ```bash
    bench get-app [YOUR_APP_GIT_REPOSITORY_URL]
    ```
    Replace `[YOUR_APP_GIT_REPOSITORY_URL]` with the actual URL of the `construction_pmis` app's Git repository. If the app is already in your `apps` folder (e.g., because you developed it there), you can skip this step.

3.  **Install the App on your Site:**
    Use the `bench --site` command to install the app on your specific ERPNext site.
    ```bash
    bench --site [your.site.name] install-app construction_pmis
    ```
    Replace `[your.site.name]` with the actual name of your ERPNext site (e.g., `myerp.localhost`, `erp.example.com`).

4.  **Migrate your Site:**
    After installing the app, run the `bench migrate` command to apply database schema changes (new DocTypes, fields, etc.) and run any patches included with the app.
    ```bash
    bench --site [your.site.name] migrate
    ```

5.  **Restart Bench (Optional but Recommended):**
    It's often a good idea to restart the bench services to ensure all changes are loaded correctly.
    ```bash
    bench restart
    ```

6.  **Clear Cache (Optional):**
    If you encounter any UI issues or old data, clearing the cache can help.
    ```bash
    bench --site [your.site.name] clear-cache
    ```
    You might also want to clear your browser cache.

## Post-Installation Steps

1.  **Verify Installation:**
    *   Log in to your ERPNext instance.
    *   You should see "Construction PMIS" in the list of modules (if a Desk Page or Workspace is configured, or by checking "Installed Applications").
    *   Try accessing some of the new DocTypes (e.g., "Project", "Cost Estimate", "Daily Log") via the Awesomebar (search bar) to ensure they are present.

2.  **Set Up Roles and Permissions:**
    *   While the app includes basic DocType permissions, you might need to:
        *   Create specific roles if they don't exist (e.g., "Project Manager", "Site Engineer", "Quantity Surveyor", "QA QC Engineer", "Safety Officer", "Contracts Manager", "Foreman", "Client Representative").
        *   Assign these roles to your users.
        *   Review and adjust permissions for each DocType based on your organization's specific needs using `Role Permissions Manager`.
        *   Configure User Permissions for record-level access if required.

3.  **Configure Workflows:**
    *   The app includes workflow definitions. Verify they are active and suit your operational processes.
    *   Navigate to "Workflow List" to see the workflows related to "Construction PMIS".
    *   You can customize these workflows (states, transitions, conditions, actions, allowed roles) as needed.

4.  **Review Numbering Series:**
    *   Most DocTypes in this app use a formatted autoname (e.g., `PROJ-{project_name}`, `RFI-{project}-{#####}`).
    *   If you need different numbering series or prefixes, you can adjust them in "Naming Series" for DocTypes that support it, or by modifying the `autoname` property in the DocType definition (requires developer mode and potentially a `bench migrate`).

5.  **Data Import (Optional):**
    *   If you have existing project data, you can use ERPNext's "Data Import" tool to import data into the new DocTypes. Prepare your data in CSV format according to the templates for each DocType.

6.  **Customization (Optional):**
    *   Customize Print Formats for documents like Payment Certificates, Variation Orders, etc.
    *   Create Custom Reports or modify existing ones.
    *   Add Custom Fields if needed.

## Troubleshooting

*   **App Not Found:** Ensure the app name `construction_pmis` is correct and that it was downloaded into the `apps` folder within your bench directory.
*   **Migration Errors:** Check the console output for specific error messages. These might relate to database issues, duplicate field names, or problems in patch files.
*   **Permission Issues:** If users can't access DocTypes, double-check Role Permissions Manager settings and ensure users have the correct roles.
*   **Bench Commands Not Working:** Make sure you are in the `frappe-bench` directory and that your bench environment is set up correctly.

For further assistance, refer to the official Frappe/ERPNext documentation or seek help from the ERPNext community forums.
---

**Note:** Replace `[YOUR_APP_GIT_REPOSITORY_URL]` and `[your.site.name]` with your actual details when using this guide.Tool output for `create_file_with_block`:
