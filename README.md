# Job Application Tracker

A Flask + MySQL web app for tracking a job search from one place. The project helps manage companies, saved jobs, submitted applications, recruiter and networking contacts, and skill-to-job matches.

## Features

- Dashboard with application, company, job, and contact metrics
- Full CRUD support for companies, jobs, applications, and contacts
- Interview notes saved in the application data
- Job match page that compares your skills against saved job requirements and shows a match percentage
- Delete confirmations for destructive actions
- Delete safeguards for companies with related jobs or contacts
- Delete safeguards for jobs with linked applications

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

## Project Layout

```text
job-application-tracker/
├── requirements.txt
├── README.md
└── job_tracker/
    ├── AI_USAGE.md
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

## Quick Start

Run these steps from the repository root unless noted otherwise.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The root `requirements.txt` delegates to `job_tracker/requirements.txt`, which remains the app-level source of truth.

3. Create the database:

   ```sql
   CREATE DATABASE job_tracker;
   ```

4. Import the schema and sample data:

   ```bash
   mysql -u root -p job_tracker < job_tracker/schema.sql
   ```

   If you already imported an older dump, recreate the database so the current schema and field names match the app.

5. Set environment variables:

   ```bash
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   export DB_NAME=job_tracker
   export DB_USER=root
   export DB_PASSWORD=your_password_here
   ```

   If your MySQL user has no password, `DB_PASSWORD` can be left empty.

6. Start the app:

   ```bash
   python3 job_tracker/app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## Notes

- `job_tracker/README.md` contains a longer project walkthrough.
- `requirements.txt` at the repo root is provided for convenience when installing from the top level.
- `job_tracker/AI_USAGE.md` documents how AI tools were used during development.
- `job_tracker/schema.sql` is the MySQL dump with populated sample records used by the app.

## Demo Asset

https://github.com/user-attachments/assets/05d2b6f0-4192-4ad1-adc8-763627d33c9a
