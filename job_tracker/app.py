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
@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies')
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=companies_list)



if __name__ == '__main__':
    app.run(debug=True)