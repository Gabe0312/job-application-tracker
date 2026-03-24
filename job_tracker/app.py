from database import get_db
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', stats=stats)


@app.route('/companies', methods = ['GET', 'POST'])
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']
        cursor.execute('INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES (%s, %s, %s, %s, %s, %s)', (name, industry, website, city, state, notes))
        conn.commit()
        return redirect('/companies')
    cursor.execute('SELECT * FROM companies')
    data = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=data)

@app.route('/jobs', methods = ['GET', 'POST'])
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['job_title']
        company_id = request.form['company_id']
        job_type = request.form['job_type']
        salary_min = request.form['salary_min']
        salary_max = request.form['salary_max']
        url = request.form['job_url']
        date_posted = request.form['date_posted']
        requirements = request.form['requirements']
        cursor.execute('INSERT INTO jobs (job_title, company_id, job_type, salary_min, salary_max, date_posted, job_url, requirements) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (title, company_id, job_type, salary_min, salary_max, date_posted, url, requirements))
        conn.commit()
        return redirect('/jobs')
    cursor.execute('''
        SELECT jobs.*, companies.company_name 
        FROM jobs 
        JOIN companies ON jobs.company_id = companies.company_id
    ''')
    data = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=data)


@app.route('/applications', methods = ['GET', 'POST'])
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        job_id = request.form['job_id']
        app_date = request.form['application_date']
        status = request.form['status']
        resume_version = request.form['resume_version']

        cover_letter_sent = 1 if 'cover_letter_sent' in request.form else 0
        
        cursor.execute('INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent) VALUES (%s, %s, %s, %s, %s)', (job_id, app_date, status, resume_version, cover_letter_sent))
        conn.commit()
        return redirect('/applications')
    cursor.execute('SELECT * FROM applications')
    data = cursor.fetchall()
    conn.close()
    return render_template('applications.html', applications=data)

@app.route('/contacts', methods = ['GET', 'POST'])
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        company_id = request.form['company_id']
        name = request.form['contact_name']
        title = request.form['title']
        email = request.form['email']
        phone = request.form['phone']
        linkedin_url = request.form['linkedin_url']
        notes = request.form['notes']
        cursor.execute('INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)', (company_id, name, title, email, phone, linkedin_url, notes))
        conn.commit()
        return redirect('/contacts')
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=data)

@app.route('/job_match', methods = ['GET', 'POST'])
def job_match():
    
    matches = []
    
    if request.method == 'POST':
        user_skills_input = request.form.get('user_skills', '')
        user_skills_list = [skill.strip().lower() for skill in user_skills_input.split(',')]
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT job_title, requirements FROM jobs')
        all_jobs = cursor.fetchall()

        for job in all_jobs:
            reqs_list = [req.strip().lower() for req in job['requirements'].split(',')]

            matched = set(user_skills_list).intersection(set(reqs_list))
            missing = set(reqs_list).difference(set(user_skills_list))

            if len(reqs_list) > 0:
                match_percentage = int((len(matched) / len(reqs_list)) * 100)
            else:
                match_percentage = 0

            if match_percentage > 0:
                matches.append({
                    'job_title': job['job_title'],
                    'match_percentage': match_percentage,
                    'matched_skills': ', '.join(matched).title(),
                    'missing_skills': ', '.join(missing).title()
                })
        matches = sorted(matches, key=lambda x: x['match_percentage'], reverse=True)
        conn.close()
    return render_template('job_match.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)