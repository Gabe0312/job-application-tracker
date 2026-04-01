import json
from database import get_db
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

CONTACT_FIELDS = (
    'company_id',
    'first_name',
    'last_name',
    'job_title',
    'email',
    'phone',
    'linkedin_url',
    'notes',
)

APPLICATION_FIELDS = (
    'job_id',
    'application_date',
    'status',
    'resume_version',
    'cover_letter_sent',
)

JOB_FIELDS = (
    'company_id',
    'job_title',
    'job_type',
    'salary_min',
    'salary_max',
    'job_url',
    'date_posted',
    'requirements',
)

COMPANY_FIELDS = (
    'company_name',
    'industry',
    'website',
    'city',
    'state',
    'notes',
)


def empty_contact_form():
    return {field: '' for field in CONTACT_FIELDS}


def contact_form_data(source):
    return {field: source.get(field, '') for field in CONTACT_FIELDS}


def empty_application_form():
    form_data = {field: '' for field in APPLICATION_FIELDS}
    form_data['interview_notes'] = ''
    return form_data


def interview_data_to_dict(value):
    if not value:
        return {}

    if isinstance(value, dict):
        return dict(value)

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {'notes': value}

        if isinstance(parsed, dict):
            return parsed

        return {'notes': str(parsed)}

    return {}


def interview_notes_from_data(value):
    notes = interview_data_to_dict(value).get('notes', '')

    if notes is None:
        return ''

    return str(notes)


def interview_data_to_json(raw_notes, existing_value=None):
    interview_data = interview_data_to_dict(existing_value)
    notes = raw_notes.strip()

    if notes:
        interview_data['notes'] = notes
    else:
        interview_data.pop('notes', None)

    return json.dumps(interview_data) if interview_data else None


def application_form_data(source):
    form_data = empty_application_form()

    for field in APPLICATION_FIELDS:
        value = source.get(field, '')

        if value is None:
            value = ''
        elif field == 'cover_letter_sent':
            value = '1' if value in (1, '1', True, 'true', 'True', 'on') else ''
        else:
            value = str(value)

        form_data[field] = value

    form_data['interview_notes'] = interview_notes_from_data(
        source.get('interview_notes', source.get('interview_data'))
    )

    return form_data


def empty_job_form():
    return {field: '' for field in JOB_FIELDS}


def job_requirements_to_text(value):
    if not value:
        return ''

    if isinstance(value, dict):
        skills = value.get('required_skills', [])
        return ', '.join(skills)

    if isinstance(value, str):
        try:
            req_dict = json.loads(value)
        except json.JSONDecodeError:
            return value

        skills = req_dict.get('required_skills', [])
        return ', '.join(skills)

    return str(value)


def job_requirements_to_json(raw_requirements):
    if raw_requirements:
        req_list = [skill.strip() for skill in raw_requirements.split(',') if skill.strip()]
    else:
        req_list = []

    return json.dumps({'required_skills': req_list})


def job_form_data(source):
    form_data = empty_job_form()

    for field in JOB_FIELDS:
        if field == 'job_url':
            value = source.get('job_url', source.get('posting_url', ''))
        elif field == 'requirements':
            value = job_requirements_to_text(source.get(field, ''))
        else:
            value = source.get(field, '')

        if value is None:
            value = ''
        elif hasattr(value, 'isoformat'):
            value = value.isoformat()
        else:
            value = str(value)

        form_data[field] = value

    return form_data


def empty_company_form():
    return {field: '' for field in COMPANY_FIELDS}


def company_form_data(source):
    return {field: source.get(field, '') for field in COMPANY_FIELDS}


def load_companies(cursor):
    cursor.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    return cursor.fetchall()


def load_company_directory(cursor):
    cursor.execute(
        '''
        SELECT companies.*,
               (SELECT COUNT(*) FROM jobs WHERE jobs.company_id = companies.company_id) AS job_count,
               (SELECT COUNT(*) FROM contacts WHERE contacts.company_id = companies.company_id) AS contact_count
        FROM companies
        ORDER BY company_name
        '''
    )
    return cursor.fetchall()


def load_contacts(cursor):
    cursor.execute('''
        SELECT contacts.*, companies.company_name
        FROM contacts
        LEFT JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.created_at DESC, contacts.contact_id DESC
    ''')
    return cursor.fetchall()


def load_jobs(cursor):
    cursor.execute('''
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        LEFT JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name, jobs.job_title
    ''')
    return cursor.fetchall()


def load_job_postings(cursor):
    cursor.execute('''
        SELECT jobs.*, companies.company_name
        FROM jobs
        LEFT JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.date_posted DESC, jobs.job_id DESC
    ''')
    jobs = cursor.fetchall()

    for job in jobs:
        if job.get('requirements'):
            try:
                job['requirements'] = json.loads(job['requirements'])
            except json.JSONDecodeError:
                job['requirements'] = {'required_skills': []}

    return jobs


def load_applications(cursor):
    cursor.execute('''
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        LEFT JOIN jobs ON applications.job_id = jobs.job_id
        LEFT JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC, applications.application_id DESC
    ''')
    applications = cursor.fetchall()

    for application in applications:
        application['interview_notes'] = interview_notes_from_data(application.get('interview_data'))

    return applications


def company_exists(cursor, company_id):
    cursor.execute('SELECT company_id FROM companies WHERE company_id = %s', (company_id,))
    return cursor.fetchone() is not None


def job_exists(cursor, job_id):
    cursor.execute('SELECT job_id FROM jobs WHERE job_id = %s', (job_id,))
    return cursor.fetchone() is not None


def job_has_applications(cursor, job_id):
    cursor.execute('SELECT 1 FROM applications WHERE job_id = %s LIMIT 1', (job_id,))
    return cursor.fetchone() is not None


def company_has_jobs(cursor, company_id):
    cursor.execute('SELECT 1 FROM jobs WHERE company_id = %s LIMIT 1', (company_id,))
    return cursor.fetchone() is not None


def company_has_contacts(cursor, company_id):
    cursor.execute('SELECT 1 FROM contacts WHERE company_id = %s LIMIT 1', (company_id,))
    return cursor.fetchone() is not None


def load_contact(cursor, contact_id):
    cursor.execute('SELECT * FROM contacts WHERE contact_id = %s', (contact_id,))
    return cursor.fetchone()


def load_application(cursor, application_id):
    cursor.execute('SELECT * FROM applications WHERE application_id = %s', (application_id,))
    return cursor.fetchone()


def load_job(cursor, job_id):
    cursor.execute('SELECT * FROM jobs WHERE job_id = %s', (job_id,))
    return cursor.fetchone()


def load_company(cursor, company_id):
    cursor.execute('SELECT * FROM companies WHERE company_id = %s', (company_id,))
    return cursor.fetchone()


def load_dashboard_stats(cursor):
    cursor.execute(
        '''
        SELECT
            (SELECT COUNT(*) FROM applications) AS applications_count,
            (SELECT COUNT(*) FROM companies) AS companies_count,
            (SELECT COUNT(*) FROM jobs) AS jobs_count,
            (SELECT COUNT(*) FROM contacts) AS contacts_count
        '''
    )
    return cursor.fetchone()


@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    stats = load_dashboard_stats(cursor)
    conn.close()
    return render_template('dashboard.html', stats=stats)


@app.route('/companies', methods = ['GET', 'POST'])
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    form_data = empty_company_form()

    if request.args.get('error') == 'delete_blocked':
        error = 'Cannot delete a company that still has linked jobs or contacts.'
    elif request.args.get('error') == 'delete_failed':
        error = 'Could not delete that company. Please try again.'
    
    if request.method == 'POST':
        form_data = company_form_data(request.form)
        cursor.execute(
            '''
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (
                form_data['company_name'],
                form_data['industry'],
                form_data['website'],
                form_data['city'],
                form_data['state'],
                form_data['notes'],
            )
        )
        conn.commit()
        conn.close()
        return redirect('/companies')

    data = load_company_directory(cursor)
    conn.close()
    return render_template(
        'companies.html',
        companies=data,
        error=error,
        form_data=form_data,
        editing_company=None,
    )


@app.route('/companies/<int:company_id>/edit', methods = ['GET', 'POST'])
def edit_company(company_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    editing_company = load_company(cursor, company_id)

    if editing_company is None:
        conn.close()
        return redirect('/companies')

    form_data = company_form_data(editing_company)

    if request.method == 'POST':
        form_data = company_form_data(request.form)
        cursor.execute(
            '''
            UPDATE companies
            SET company_name = %s,
                industry = %s,
                website = %s,
                city = %s,
                state = %s,
                notes = %s
            WHERE company_id = %s
            ''',
            (
                form_data['company_name'],
                form_data['industry'],
                form_data['website'],
                form_data['city'],
                form_data['state'],
                form_data['notes'],
                company_id,
            )
        )
        conn.commit()
        conn.close()
        return redirect('/companies')

    data = load_company_directory(cursor)
    conn.close()
    return render_template(
        'companies.html',
        companies=data,
        error=error,
        form_data=form_data,
        editing_company=editing_company,
    )


@app.route('/companies/<int:company_id>/delete', methods = ['POST'])
def delete_company(company_id):
    conn = get_db()
    cursor = conn.cursor()

    if company_has_jobs(cursor, company_id) or company_has_contacts(cursor, company_id):
        conn.close()
        return redirect('/companies?error=delete_blocked')

    try:
        cursor.execute('DELETE FROM companies WHERE company_id = %s', (company_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        return redirect('/companies?error=delete_failed')

    conn.close()
    return redirect('/companies')

@app.route('/jobs', methods = ['GET', 'POST'])
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    form_data = empty_job_form()
    companies = load_companies(cursor)

    if request.args.get('error') == 'delete_blocked':
        error = 'Cannot delete a job that already has applications.'
    
    if request.method == 'POST':
        form_data = job_form_data(request.form)

        if not company_exists(cursor, form_data['company_id']):
            error = 'Select a valid company before adding a job.'
        else:
            cursor.execute(
                '''
                INSERT INTO jobs (job_title, company_id, job_type, salary_min, salary_max, date_posted, posting_url, requirements)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (
                    form_data['job_title'],
                    form_data['company_id'],
                    form_data['job_type'],
                    form_data['salary_min'] or None,
                    form_data['salary_max'] or None,
                    form_data['date_posted'] or None,
                    form_data['job_url'],
                    job_requirements_to_json(form_data['requirements']),
                )
            )
            conn.commit()
            conn.close()
            return redirect('/jobs')

    data = load_job_postings(cursor)
    conn.close()
    return render_template(
        'jobs.html',
        jobs=data,
        companies=companies,
        error=error,
        form_data=form_data,
        editing_job=None,
    )


@app.route('/jobs/<int:job_id>/edit', methods = ['GET', 'POST'])
def edit_job(job_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    companies = load_companies(cursor)
    editing_job = load_job(cursor, job_id)

    if editing_job is None:
        conn.close()
        return redirect('/jobs')

    form_data = job_form_data(editing_job)

    if request.method == 'POST':
        form_data = job_form_data(request.form)

        if not company_exists(cursor, form_data['company_id']):
            error = 'Select a valid company before saving this job.'
        else:
            cursor.execute(
                '''
                UPDATE jobs
                SET company_id = %s,
                    job_title = %s,
                    job_type = %s,
                    salary_min = %s,
                    salary_max = %s,
                    date_posted = %s,
                    posting_url = %s,
                    requirements = %s
                WHERE job_id = %s
                ''',
                (
                    form_data['company_id'],
                    form_data['job_title'],
                    form_data['job_type'],
                    form_data['salary_min'] or None,
                    form_data['salary_max'] or None,
                    form_data['date_posted'] or None,
                    form_data['job_url'],
                    job_requirements_to_json(form_data['requirements']),
                    job_id,
                )
            )
            conn.commit()
            conn.close()
            return redirect('/jobs')

    data = load_job_postings(cursor)
    conn.close()
    return render_template(
        'jobs.html',
        jobs=data,
        companies=companies,
        error=error,
        form_data=form_data,
        editing_job=editing_job,
    )


@app.route('/jobs/<int:job_id>/delete', methods = ['POST'])
def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()

    if job_has_applications(cursor, job_id):
        conn.close()
        return redirect('/jobs?error=delete_blocked')

    cursor.execute('DELETE FROM jobs WHERE job_id = %s', (job_id,))
    conn.commit()
    conn.close()
    return redirect('/jobs')


@app.route('/applications', methods = ['GET', 'POST'])
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    form_data = empty_application_form()
    jobs = load_jobs(cursor)
    
    if request.method == 'POST':
        form_data = application_form_data(request.form)

        if not job_exists(cursor, form_data['job_id']):
            error = 'Select a valid job before adding an application.'
        else:
            cursor.execute(
                '''
                INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (
                    form_data['job_id'],
                    form_data['application_date'],
                    form_data['status'],
                    form_data['resume_version'],
                    1 if form_data['cover_letter_sent'] else 0,
                    interview_data_to_json(form_data['interview_notes']),
                )
            )
            conn.commit()
            conn.close()
            return redirect('/applications')

    data = load_applications(cursor)
    conn.close()
    return render_template(
        'applications.html',
        applications=data,
        jobs=jobs,
        error=error,
        form_data=form_data,
        editing_application=None,
    )


@app.route('/applications/<int:application_id>/edit', methods = ['GET', 'POST'])
def edit_application(application_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    jobs = load_jobs(cursor)
    editing_application = load_application(cursor, application_id)

    if editing_application is None:
        conn.close()
        return redirect('/applications')

    form_data = application_form_data(editing_application)

    if request.method == 'POST':
        form_data = application_form_data(request.form)

        if not job_exists(cursor, form_data['job_id']):
            error = 'Select a valid job before saving this application.'
        else:
            cursor.execute(
                '''
                UPDATE applications
                SET job_id = %s,
                    application_date = %s,
                    status = %s,
                    resume_version = %s,
                    cover_letter_sent = %s,
                    interview_data = %s
                WHERE application_id = %s
                ''',
                (
                    form_data['job_id'],
                    form_data['application_date'],
                    form_data['status'],
                    form_data['resume_version'],
                    1 if form_data['cover_letter_sent'] else 0,
                    interview_data_to_json(
                        form_data['interview_notes'],
                        editing_application.get('interview_data'),
                    ),
                    application_id,
                )
            )
            conn.commit()
            conn.close()
            return redirect('/applications')

    data = load_applications(cursor)
    conn.close()
    return render_template(
        'applications.html',
        applications=data,
        jobs=jobs,
        error=error,
        form_data=form_data,
        editing_application=editing_application,
    )


@app.route('/applications/<int:application_id>/delete', methods = ['POST'])
def delete_application(application_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM applications WHERE application_id = %s', (application_id,))
    conn.commit()
    conn.close()
    return redirect('/applications')

@app.route('/contacts', methods = ['GET', 'POST'])
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    form_data = empty_contact_form()
    companies = load_companies(cursor)
    
    if request.method == 'POST':
        form_data = contact_form_data(request.form)

        if not company_exists(cursor, form_data['company_id']):
            error = 'Select a valid company before adding a contact.'
        else:
            cursor.execute(
                'INSERT INTO contacts (company_id, first_name, last_name, job_title, email, phone, linkedin_url, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    form_data['company_id'],
                    form_data['first_name'],
                    form_data['last_name'],
                    form_data['job_title'],
                    form_data['email'],
                    form_data['phone'],
                    form_data['linkedin_url'],
                    form_data['notes'],
                )
            )
            conn.commit()
            conn.close()
            return redirect('/contacts')
    data = load_contacts(cursor)
    conn.close()
    return render_template(
        'contacts.html',
        contacts=data,
        companies=companies,
        error=error,
        form_data=form_data,
        editing_contact=None,
    )


@app.route('/contacts/<int:contact_id>/edit', methods = ['GET', 'POST'])
def edit_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    error = None
    companies = load_companies(cursor)
    editing_contact = load_contact(cursor, contact_id)

    if editing_contact is None:
        conn.close()
        return redirect('/contacts')

    form_data = contact_form_data(editing_contact)

    if request.method == 'POST':
        form_data = contact_form_data(request.form)

        if not company_exists(cursor, form_data['company_id']):
            error = 'Select a valid company before saving this contact.'
        else:
            cursor.execute(
                '''
                UPDATE contacts
                SET company_id = %s,
                    first_name = %s,
                    last_name = %s,
                    job_title = %s,
                    email = %s,
                    phone = %s,
                    linkedin_url = %s,
                    notes = %s
                WHERE contact_id = %s
                ''',
                (
                    form_data['company_id'],
                    form_data['first_name'],
                    form_data['last_name'],
                    form_data['job_title'],
                    form_data['email'],
                    form_data['phone'],
                    form_data['linkedin_url'],
                    form_data['notes'],
                    contact_id,
                )
            )
            conn.commit()
            conn.close()
            return redirect('/contacts')

    data = load_contacts(cursor)
    conn.close()
    return render_template(
        'contacts.html',
        contacts=data,
        companies=companies,
        error=error,
        form_data=form_data,
        editing_contact=editing_contact,
    )

@app.route('/contacts/<int:contact_id>/delete', methods = ['POST'])
def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE contact_id = %s', (contact_id,))
    conn.commit()
    conn.close()
    return redirect('/contacts')

@app.route('/job_match', methods = ['GET', 'POST'])
def job_match():
    
    matches = []
    
    if request.method == 'POST':
        user_skills_input = request.form.get('user_skills', '')
        user_skills_list = [skill.strip().lower() for skill in user_skills_input.split(',')]
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''SELECT job_title, jobs.requirements, companies.company_name
                          FROM jobs
                          JOIN companies ON jobs.company_id = companies.company_id
        ''')
        all_jobs = cursor.fetchall()

        for job in all_jobs:
            
            if not job['requirements']:
                continue
            try:
                req_dict = json.loads(job['requirements'])
            except json.JSONDecodeError:
                continue
            
            raw_reqs_list = req_dict.get('required_skills', [])
            
            reqs_list = [req.strip().lower() for req in raw_reqs_list]
            
            matched = set(user_skills_list).intersection(set(reqs_list))
            missing = set(reqs_list).difference(set(user_skills_list))

            if len(reqs_list) > 0:
                match_percentage = int((len(matched) / len(reqs_list)) * 100)
            else:
                match_percentage = 0

            if match_percentage > 0:
                matches.append({
                    'job_title': job['job_title'],
                    'company_name': job['company_name'],
                    'match_percentage': match_percentage,
                    'matched_skills': ', '.join(matched).title(),
                    'missing_skills': ', '.join(missing).title()
                })
        matches = sorted(matches, key=lambda x: x['match_percentage'], reverse=True)
        conn.close()
    return render_template('job_match.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
