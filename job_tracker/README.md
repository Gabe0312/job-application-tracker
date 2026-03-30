# Job Application Tracker

Job Application Tracker is a Flask + MySQL app for organizing a job search in one place. It helps you keep track of target companies, saved roles, submitted applications, networking contacts, and skill-to-job matches.

## What It Does

- Shows a dashboard with a total application count and quick links
- Lets you add, edit, list, and delete companies
- Lets you add, edit, list, and delete job postings
- Lets you add, edit, list, and delete applications
- Lets you add, edit, list, and delete contacts
- Compares your skills against saved job requirements on the job match page
- Prevents deleting companies that still have jobs or contacts
- Prevents deleting jobs that already have linked applications

## Tech Stack

- Python
- Flask
- MySQL
- HTML templates
- CSS

## Project Structure

```text
job_tracker/
├── app.py
├── database.py
├── requirements.txt
├── schema.sql
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── companies.html
    ├── jobs.html
    ├── applications.html
    ├── contacts.html
    └── job_match.html
```

## Setup

Run these steps from the `job_tracker` directory.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create the MySQL database:

   ```sql
   CREATE DATABASE job_tracker;
   ```

4. Load the final populated database dump:

   ```bash
   mysql -u root -p job_tracker < schema.sql
   ```

   `schema.sql` is a MySQL Workbench dump of the completed project database. Importing it recreates the tables and loads the saved records used by the app.

5. Set database environment variables for the machine where you are running the app:

   ```bash
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   export DB_NAME=job_tracker
   export DB_USER=root
   export DB_PASSWORD=your_password_here
   ```

6. Start the app:

   ```bash
   python app.py or python3 app.py
   ```

7. Open `http://127.0.0.1:5000`.

## Main Pages

- `/` dashboard
- `/companies` company directory
- `/jobs` saved job postings
- `/applications` application tracker
- `/contacts` contact manager
- `/job_match` skill match tool

## Data Notes

- Job requirements are entered as comma-separated skills in the UI and stored as JSON in the `jobs.requirements` column.
- Jobs must belong to an existing company.
- Applications must belong to an existing job.
- Contacts must belong to an existing company.
- `schema.sql` contains both the schema and populated sample data from the final project database.
- The schema includes a few extra columns that are not currently managed through the UI, so `schema.sql` is the source of truth for the database shape.

## Development Notes

- The app runs with Flask's built-in development server from `app.py`.
- The current entry point starts Flask with `debug=True`.
