from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# DATABASE MODELS
# =========================

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    college = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    year = db.Column(db.String(20))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    rating = db.Column(db.Integer)

# =========================
# SCREEN 1 - HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template('home.html')

# =========================
# SCREEN 2 - REGISTRATION
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        college = request.form['college']
        branch = request.form['branch']
        year = request.form['year']

        student = Student(
            fullname=fullname,
            email=email,
            password=password,
            college=college,
            branch=branch,
            year=year
        )

        db.session.add(student)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')
# =========================
# SCREEN 3 - LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        student = Student.query.filter_by(email=email, password=password).first()

        if student:
            return redirect('/profile')
        else:
            return 'Invalid Email or Password'

    return render_template('login.html')

# =========================
# SCREEN 4 - STUDENT PROFILE INPUT
# =========================
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        tenth = request.form['tenth']
        twelfth = request.form['twelfth']
        cgpa = request.form['cgpa']
        skills = request.form.getlist('skills')
        career_goal = request.form['career_goal']
        interest = request.form['interest']
        study_hours = request.form['study_hours']

        print('10th %:', tenth)
        print('12th %:', twelfth)
        print('CGPA:', cgpa)
        print('Skills:', skills)
        print('Career Goal:', career_goal)
        print('Interest:', interest)
        print('Study Hours:', study_hours)

        return redirect('/skill-gap')

    return render_template('profile.html')

# =========================
# SCREEN 5 - SKILL GAP ANALYSIS
# =========================
@app.route('/skill-gap')
def skill_gap():

    your_skills = ['Java', 'HTML', 'CSS']

    required_skills = [
        'Java',
        'Spring Boot',
        'SQL',
        'JavaScript',
        'React'
    ]

    missing_skills = []

    for skill in required_skills:
        if skill not in your_skills:
            missing_skills.append(skill)

    return render_template(
        'skill_gap.html',
        your_skills=your_skills,
        required_skills=required_skills,
        missing_skills=missing_skills
    )

# =========================
# SCREEN 6 - LEARNING ROADMAP
# =========================
@app.route('/roadmap')
def roadmap():

    roadmap_data = {
        'Phase 1': ['Core Java', 'SQL Basics', 'HTML & CSS'],
        'Phase 2': ['Spring Boot', 'JavaScript', 'Database Integration'],
        'Phase 3': ['React Basics', 'Mini Project', 'Internship Prep']
    }

    return render_template('roadmap.html', roadmap=roadmap_data)

# =========================
# SCREEN 7 - PROJECT & INTERNSHIP
# =========================

@app.route('/projects')
def projects():

    mini_projects = [
        'Student Management System',
        'Online Quiz Application'
    ]

    major_project = 'AI-Based Learning Roadmap System'

    internships = [
        'Java Developer Intern',
        'Full Stack Intern'
    ]
    return render_template(
        'projects.html',
        mini_projects=mini_projects,
        major_project=major_project,
        internships=internships
    )

# =========================
# SCREEN 8 - PROGRESS DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    progress = {
        'skills_completed': '60%',
        'tasks_done': '8/10',
        'hours_studied': '15 hrs'
    }

    return render_template('dashboard.html', progress=progress)

# =========================
# SCREEN 9 - ADMIN DASHBOARD
# =========================

@app.route('/admin')
def admin():

    students = Student.query.all()

    return render_template('admin.html', students=students)
# =========================
# SCREEN 10 - FEEDBACK
# =========================

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    if request.method == 'POST':
        message = request.form['message']
        rating = request.form['rating']

        new_feedback = Feedback(
            message=message,
            rating=rating
        )

        db.session.add(new_feedback)
        db.session.commit()

        return 'Feedback Submitted Successfully'

    return render_template('feedback.html')

# =========================
# MAIN FUNCTION
# =========================
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)