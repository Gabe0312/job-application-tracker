# Job Application Tracker

A Flask + MySQL web app for tracking a job search from one place. The project helps manage companies, saved jobs, submitted applications, recruiter and networking contacts, and skill-to-job matches.

## Features

- Dashboard with application, company, job, and contact metrics
- Full CRUD support for companies, jobs, applications, and contacts
- Interview notes saved in the application data
- Job match page that compares your skills against saved job requirements and shows a match percentage
- Delete safeguards for companies with related jobs or contacts
- Delete safeguards for jobs with linked applications

## Tech Stack

- Python
- Flask
- MySQL
- HTML templates
- CSS

## Project Layout

```text
job-application-tracker/
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

Run these steps from the `job_tracker` directory.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create the database:

   ```sql
   CREATE DATABASE job_tracker;
   ```

4. Import the schema and sample data:

   ```bash
   mysql -u root -p job_tracker < schema.sql
   ```

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
   python3 app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## Notes

- `job_tracker/README.md` contains a longer project walkthrough.
- `job_tracker/AI_USAGE.md` documents how AI tools were used during development.
- `job_tracker/schema.sql` includes both the table definitions and populated sample records.

## Demo Asset

https://github.com/user-attachments/assets/05d2b6f0-4192-4ad1-adc8-763627d33c9a
