# Daily Activity Portal

This project is a web-based portal for tracking the daily activities of team members. It provides role-based dashboards, activity logging, progress tracking, and reporting features for managers and super admins.

## Features

- **Role-Based Access Control**: Different views and permissions for Super Admins, Team Managers, and Team Members.
- **Activity Management**: Create, update, and assign activities.
- **Daily Updates**: Log daily progress on activities.
- **Dashboards**: At-a-glance overview of activities, with search and filtering.
- **Reporting**: Generate reports on team and individual performance.
- **Data Export**: Export reports to Excel.

## Technology Stack

- **Backend**: Django
- **Frontend**: Django Templates, Bootstrap
- **Database**: PostgreSQL
- **Deployment**: Docker, Gunicorn, Nginx

## Setup and Installation

This project is fully containerized using Docker. To run the application, you will need to have Docker and Docker Compose installed on your machine.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create an environment file:**
    Create a `.env` file in the project root by copying the example:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your desired settings. A `SECRET_KEY` is required. You can generate one using Django's `get_random_secret_key()` function.

3.  **Build and run the containers:**
    ```bash
    sudo docker compose up --build -d
    ```
    This will build the Docker images and start the containers for the Django application, PostgreSQL database, and Nginx reverse proxy.

4.  **Create database migrations:**
    The first time you run the application, you will need to create and apply the database migrations:
    ```bash
    sudo docker compose exec web python manage.py makemigrations
    sudo docker compose exec web python manage.py migrate
    ```

5.  **Create a superuser:**
    To access the Django admin, you will need to create a superuser:
    ```bash
    sudo docker compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to create your superuser account.

## Usage

-   **Access the application**: Open your web browser and navigate to `http://localhost:80`.
-   **Admin Panel**: Access the Django admin at `http://localhost:80/admin/`.
-   **Sign up**: New users can sign up for an account. By default, new accounts are inactive and must be activated by an admin in the Django admin panel.
-   **User Roles**:
    -   **Team Member**: Can log and update their own activities. Can assign activities to other members.
    -   **Team Manager**: Can manage a single team, assign activities, manage dropdown values, and generate team-level reports.
    -   **Super Admin**: Has full control over the system, can manage multiple teams, and generate system-wide reports.

## Running the Application

To start the application:
```bash
sudo docker compose up -d
```

To stop the application:
```bash
sudo docker compose down
```
To view the logs:
```bash
sudo docker compose logs -f
```

## Seeding Initial Data
The SRS specifies that there should be a seed script or fixtures for default dropdown values, sample users, and test activities. This has not been implemented yet.
To manually seed the data, you can use the Django admin panel to create:
1.  **Dropdown values**: Go to the `Dropdowns` section and add some `Node Names`, `Activity Types`, and `Statuses`. For example, for Status, you could add "To Do", "In Progress", and "Completed".
2.  **Users**: Create some users with different roles.
3.  **Teams**: Create a team and assign a manager and members.
4.  **Activities**: Create some activities and assign them to users.

This will populate the application with some initial data to work with.
