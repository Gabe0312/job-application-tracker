# Job Application Tracker

Job Application Tracker is a Flask + MySQL app for organizing a job search in one place. It helps you keep track of target companies, saved roles, submitted applications, networking contacts, and skill-to-job matches.

## What It Does

- Shows a dashboard with application, company, job, and contact metrics plus quick links
- Lets you add, edit, list, and delete companies
- Lets you add, edit, list, and delete job postings
- Lets you add, edit, list, and delete applications
- Lets you add, edit, list, and delete contacts
- Compares your skills against saved job requirements on the job match page
- Prompts for confirmation before destructive deletes
- Prevents deleting companies that still have jobs or contacts
- Prevents deleting jobs that already have linked applications

## Tech Stack

- Python
- Flask
- MySQL
- HTML templates
- CSS

## Prerequisites

- Python 3 with `pip`
- A local MySQL server
- The `mysql` command-line client for importing `schema.sql`

## Project Structure

```text
job_tracker/
├── app.py
├── database.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── jobs.html
│   ├── applications.html
│   ├── contacts.html
│   └── job_match.html
├── static/
│   └── style.css
├── schema.sql
├── AI_USAGE.md
├── README.md
└── requirements.txt
```

`config.py` is created locally from `config.example.py` during setup and is ignored by Git, so it is not part of the committed project structure.

## Setup

Run these steps from the `job_tracker` directory.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If you prefer to install from the repository root, use `pip install -r ../requirements.txt` instead.

3. Create the MySQL database:

   ```sql
   CREATE DATABASE job_tracker;
   ```

4. Load the final populated database dump:

   ```bash
   mysql -u root -p job_tracker < schema.sql
   ```

   `schema.sql` is the MySQL dump for the completed project database. Importing it recreates the tables and loads the saved records used by the app.

5. Create a local database config file:

   ```bash
   cp config.example.py config.py
   ```

6. Edit `config.py` and set your local MySQL credentials:

   ```python
   DB_HOST = '127.0.0.1'
   DB_USER = 'root'
   DB_PASSWORD = 'your_password_here'
   DB_NAME = 'job_tracker'
   DB_PORT = 3306
   ```

   `config.py` is ignored by Git so your real password is not committed. For course submission, provide the password separately in Canvas as instructed by your professor.

7. Start the app:

   ```bash
   python3 app.py
   ```

8. Open `http://127.0.0.1:5000`.

## Main Pages

- `/` dashboard
- `/companies` company directory
- `/jobs` saved job postings
- `/applications` application tracker
- `/contacts` contact manager
- `/job_match` skill match tool

## Data Notes

- Job requirements are entered as comma-separated skills in the UI and stored as JSON in the `jobs.requirements` column.
- Interview notes are stored in the `applications.interview_data` JSON column.
- Jobs must belong to an existing company.
- Applications must belong to an existing job.
- Contacts must belong to an existing company.
- `schema.sql` contains both the schema and populated sample data from the final project database.
- The schema reflects the MySQL dump currently used by the app, including legacy columns such as `jobs.posting_url` and `contacts.first_name` / `contacts.last_name`.

## Development Notes

- The app runs with Flask's built-in development server from `app.py`.
- The current entry point starts Flask with `debug=True`.
