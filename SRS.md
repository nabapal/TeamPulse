Software Requirements Specification (SRS)

Project Name: Daily Activity Portal (Team Work Tracker)

1. Introduction
1.1 Purpose

The purpose of this project is to create a web-based portal for tracking daily activities of team members.
The system will enable role-based dashboards, activity logging, progress tracking, and detailed reporting for team members, managers, and leads.

1.2 Scope

Team Members log and update their daily tasks.

Team Managers (Admins) monitor, assign, and report on activities for one or more teams.

Lead oversees all teams across the system and has the highest level of control.

The portal provides:

Real-time dashboards

Historical updates

Weekly & monthly reporting tabs

Exportable reports

1.3 Definitions

Activity: A task logged by a user, assigned to one or more members.

Update: A daily progress entry for an activity.

Node Name / Activity Type / Status: Configurable dropdown values.

2. User Roles & Permissions
2.1 Lead

Manage multiple teams across the system.

Full CRUD (Create, Read, Update, Delete) on activities and dropdowns.

Generate system-wide daily, weekly, and monthly reports.

Assign activities to any user/team.

2.2 Team Manager (Admin)

Manage one or more teams.

Assign activities to one/multiple members.

Add/update/delete dropdown values (Node Name, Activity Type, Status).

Generate team-level daily, weekly, and monthly reports.

Modify Node Name & Activity Type of activities.

View all historical updates with assignee details.

2.3 Team Member

Log and update personal activities.

Assign activities to other team members (within the team).

Modify any of their activities.

Cannot delete activities.

View dashboard restricted to own tasks.

Generate personal daily, weekly, and monthly reports.

3. Functional Requirements
3.1 Authentication & User Management

User signup/login with role-based access.

Password reset/change.

Admin approval for new accounts.

Team-based grouping of users.

3.2 Activity Management

Fields:

Auto-generated Activity ID

Description (text input)

Node Name (dropdown)

Activity Type (dropdown: In Progress, Completed, Yet to Start, On Hold)

Status (dropdown: in_progress, completed, yet_to_start, on_hold)

Start Date (calendar)

End Date (calendar)

Duration (auto-calculated)

Daily Updates (historical logging with date selection)

Assigned Users (multi-select)

Rules:

Members cannot delete activities.

Managers & Lead can delete activities.

Daily updates tagged with username (for multi-assignees).

3.3 Dashboard

Member Dashboard: Shows only own activities (active upfront, historical in sidebar).

Manager Dashboard: Overview of all assigned team activities.

Lead Dashboard: Overview of all teams.

Features:

Search by keyword.

Filters by status, activity type, node name, assignee, date range.

Pie chart of activities by status.

Tabs for Daily / Weekly / Monthly Reports.

3.4 Daily Updates

Users can add/update daily progress logs.

Updates are date-specific (backlog allowed).

Audit trail of who updated and when.

3.5 Reporting

Reports available for Members, Managers, and Leads:

Daily Report → Activities logged/updated on a given day.

Weekly Report → Aggregated view for past 7 days.

Monthly Report → Trend charts + KPI summaries.

KPIs:

Activity count by status (In Progress, Completed, On Hold).

Workload distribution by user.

Average duration per activity.

% completed on-time vs overdue.

Export options:

Excel (openpyxl)

PDF (reportlab)

Print-friendly HTML

CSV + JSON for integration

3.6 Admin Features

CRUD operations on dropdown values (Node, Activity Type, Status).

Assign activities to one or multiple members.

Delete/update activities.

View all historical updates with assignee details.

4. Non-Functional Requirements

Scalability: Support hundreds of daily activities across multiple teams.

Performance: Dashboards must load within 2 seconds for up to 1000 records.

Security: Role-based access control, secure password storage, session management.

Usability: Clean UI with CoreUI Bootstrap 5 components, calendar views, easy navigation.

Reliability: No activity loss; updates stored with timestamps.

5. UI/UX Requirements

CoreUI Bootstrap 5 as frontend framework.

Intuitive dashboards with tabs: Active vs History.

Calendar integration for date selection.

Pie charts and tables for visualization.

Search bar + filter dropdowns for activity navigation.

Export buttons (Excel / CSV / JSON / PDF / Print).

Color scheme for status:

Green = Completed

Yellow = In Progress

Red = On Hold

Blue = Yet to Start

6. System Flow

User logs in → redirected to role-based dashboard.

Member adds/updates activity.

Manager assigns/reviews team activities.

Lead monitors across teams.

Reports generated and exported as needed.

7. Deliverables (Django + Docker)
Backend

Django project with modular apps:

users (authentication, roles, approval flow)

teams (team management)

activities (activity CRUD & rules)

updates (daily updates & history)

dashboard (role-based dashboards)

reports (reporting & exports)

dropdowns (configurable Node, Activity Type, Status)

Django ORM models for Users, Teams, Activities, Updates, Dropdowns.

Role-based access control using Django auth + permissions.

Business rules:

Members cannot delete activities.

Updates must always include user + timestamp.

Django Admin customization for Managers & Lead.

Frontend (Django Templates + CoreUI Bootstrap 5)

Role-based dashboards (Member → personal, Manager → team, Lead → all teams).

UI Features: Search bar, filters, calendar pickers, pie charts, export buttons, reporting tabs.

Database

PostgreSQL as production DB.

Proper indexing for high-performance queries.

Migrations via makemigrations & migrate.

Seed script for dummy data:

1 Lead

4 Managers

Teams: Telco, IPSE, IP-MPLS-Access, IP-MPLS-Core, FTTX, Enterprise, Optical, Microwave-Clocking

5 Members per team

Each member has 10 activities (6 solo, 4 multi-assigned).

Reporting & Exports

Daily, Weekly, Monthly reports.

Exports to Excel, PDF, CSV, JSON.

Deployment (Docker Setup)

Dockerized application with separate containers:

Django backend

PostgreSQL database

Nginx reverse proxy

Gunicorn as WSGI server.

.env file for secrets.

Persistent DB storage.

Logging & monitoring enabled.

8. Documentation

Detailed README.md for running project in Docker.

Postman collection or OpenAPI docs for APIs.

Developer notes for extending dropdowns, roles, or reports.
